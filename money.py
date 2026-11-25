"""Manifest-driven research CLI: money.py test|replay|compare|mc. See docs/strategies.md."""
import argparse
import hashlib
import importlib
import json
import math
import re
import sys
from datetime import date, timedelta
from pathlib import Path
import compare as compare_reports
import harness
from spot import Spot, spot_fixture
from stress import StressConfig

FIELDS = {"id", "version", "entry", "data", "calendar", "warmup", "levels", "costs", "benchmark", "max_exposure"}
OPTIONAL = {"allow_short", "borrow_bps_per_year", "walk_forward"}
BORROW_BPS = 50.  # annual, same general-collateral default as xsection.Costs
KINDS = {"fixture": "xnys", "spot_fixture": "utc24", "alpaca": "xnys", "kraken": "utc24"}
START_CASH = 10000.


class ManifestError(ValueError):
    pass


def is_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def load_manifest(path):
    """Validate the whole manifest and return it, or raise one ManifestError listing every problem."""
    path = Path(path)
    try:
        m = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ManifestError(f"{path}: cannot read manifest: {exc}") from exc
    if not isinstance(m, dict):
        raise ManifestError(f"{path}: manifest must be a JSON object")
    errors = [f"missing field: {k}" for k in sorted(FIELDS - m.keys())]
    errors += [f"unknown field: {k}" for k in sorted(m.keys() - FIELDS - OPTIONAL)]
    for key in ("id", "version", "benchmark"):
        if key in m and not (isinstance(m[key], str) and m[key].strip()):
            errors.append(f"{key} must be a non-empty string")
    if isinstance(m.get("id"), str) and m["id"].strip() and not re.fullmatch(r"[A-Za-z0-9_.-]+", m["id"]):
        errors.append("id may only contain letters, digits, '_', '.' and '-'")
    calendar = m.get("calendar")
    if "calendar" in m and calendar not in ("xnys", "utc24"):
        errors.append("calendar must be 'xnys' or 'utc24'")
    if "warmup" in m and (type(m["warmup"]) is not int or m["warmup"] < 0):
        errors.append("warmup must be a nonnegative integer")
    levels = m.get("levels")
    if "levels" in m:
        if not isinstance(levels, list) or not levels or not all(map(is_number, levels)):
            errors.append("levels must be a non-empty list of finite numbers")
        elif len(set(levels)) != len(levels):
            errors.append("levels must be distinct")
    if "walk_forward" in m and harness.check_walk_forward(m["walk_forward"]):
        errors.append(harness.check_walk_forward(m["walk_forward"]))
    if "allow_short" in m and type(m["allow_short"]) is not bool:
        errors.append("allow_short must be true or false")
    if "borrow_bps_per_year" in m:
        if not (is_number(m["borrow_bps_per_year"]) and m["borrow_bps_per_year"] >= 0):
            errors.append("borrow_bps_per_year must be a finite number >= 0")
        if m.get("allow_short") is not True:
            errors.append("borrow_bps_per_year needs allow_short true")
    if m.get("allow_short") is True and m.get("costs") != "equity_ibkr":
        errors.append("allow_short is modelled for costs 'equity_ibkr' only")
    exposure = m.get("max_exposure")
    if "max_exposure" in m and not (is_number(exposure) and 0 < exposure <= 1):
        errors.append("max_exposure must be a finite number in (0, 1]")
    data = m.get("data")
    if "data" in m:
        if not isinstance(data, dict) or set(data) != {"kind", "symbol"}:
            errors.append("data must be an object with exactly 'kind' and 'symbol'")
        elif data["kind"] not in KINDS:
            errors.append(f"data.kind must be one of {sorted(KINDS)}")
        elif not (isinstance(data["symbol"], str) and data["symbol"].strip()):
            errors.append("data.symbol must be a non-empty string")
        elif calendar in ("xnys", "utc24") and KINDS[data["kind"]] != calendar:
            errors.append(f"data.kind '{data['kind']}' is a {KINDS[data['kind']]} source but calendar is '{calendar}'")
    costs = m.get("costs")
    if "costs" in m:
        profile = None
        if costs == "equity_ibkr":
            profile = "xnys"
        elif isinstance(costs, dict) and set(costs) == {"fee_bps", "lot", "min_usd"}:
            profile = "utc24"
            if not all(map(is_number, costs.values())):
                errors.append("costs.fee_bps, lot and min_usd must be finite numbers")
            else:
                try:
                    Spot(costs["fee_bps"], costs["lot"], costs["min_usd"])
                except ValueError as exc:
                    errors.append(f"costs: {exc}")
        else:
            errors.append("costs must be 'equity_ibkr' or an object with fee_bps, lot and min_usd")
        if profile and calendar in ("xnys", "utc24") and profile != calendar:
            errors.append(f"costs are for the {profile} calendar but calendar is '{calendar}'")
    entry = m.get("entry")
    if "entry" in m:
        if not (isinstance(entry, str) and re.fullmatch(r"[\w.]+:\w+", entry)):
            errors.append("entry must look like 'module:name'")
        else:
            module, name = entry.split(":")
            # The manifest's folder is importable so an unseen package runs without editing the runner.
            folder = str(path.resolve().parent)
            if folder in sys.path:
                sys.path.remove(folder)
            sys.path.insert(0, folder)
            own = Path(folder) / f"{module.split('.')[0]}.py"
            cached = sys.modules.get(module)
            # Catalog folders all name their file strategy.py: drop another folder's cached module of that name.
            if own.exists() and cached is not None and Path(getattr(cached, "__file__", None) or "").resolve() != own.resolve():
                del sys.modules[module]
            try:
                target = getattr(importlib.import_module(module), name)
                if not callable(getattr(target, "decide", target)) or not callable(getattr(target, "fit", print)):
                    errors.append(f"entry {entry} is not a callable decision function (or fit/decide pair)")
            except (ImportError, AttributeError) as exc:
                errors.append(f"entry {entry} cannot be imported: {exc}")
    if errors:
        raise ManifestError(f"Invalid manifest {path}:\n" + "\n".join(f"  - {e}" for e in errors))
    return m


class Plugin:
    """Applies warmup abstention and the exposure cap around a strategy, keeping its optional fit."""

    def __init__(self, manifest):
        module, name = manifest["entry"].split(":")
        inner = getattr(importlib.import_module(module), name)
        self.inner = getattr(inner, "decide", inner)
        if hasattr(inner, "fit"):
            self.fit = inner.fit
        self.warmup = manifest["warmup"]
        self.exposure = manifest["max_exposure"]
        self.lot = manifest["costs"]["lot"] if isinstance(manifest["costs"], dict) else 1

    def __call__(self, history, parameter):
        if len(history) < self.warmup:
            return None
        target = self.inner(history, parameter)
        if type(target) is int:
            # Cap is measured against starting cash at the last close, not live equity.
            cap = int(self.exposure * START_CASH / (self.lot * history[-1]))
            target = max(min(target, cap), -cap)
        return target

    decide = __call__


def short_rate(manifest):
    return manifest.get("borrow_bps_per_year", BORROW_BPS) if manifest.get("allow_short") else None


def spot_costs(manifest):
    costs = manifest["costs"]
    return Spot(costs["fee_bps"], costs["lot"], costs["min_usd"]) if isinstance(costs, dict) else None


def load_rows(manifest, start, end):
    kind = manifest["data"]["kind"]
    if kind == "fixture":
        return harness.fixture(), kind, {}
    if kind == "spot_fixture":
        return spot_fixture(), kind, {}
    if kind == "kraken":
        from kraken_bars import daily_from_kraken
        rows, quality = daily_from_kraken(manifest["data"]["symbol"])
        return rows, "kraken_ohlc", quality
    from alpaca_bars import daily_from_alpaca
    rows, quality = daily_from_alpaca(manifest["data"]["symbol"], harness.months_after(start, -12), end, "sip", Path("data/alpaca"), False)
    return rows, "alpaca_sip_raw", quality


def run_test(manifest, start, end, paths, shock_bps, seed, mc=None):
    if start.day != 1 or paths < 1 or not math.isfinite(shock_bps) or shock_bps < 0:
        raise ValueError("Use a month-start date, positive path count and finite shock")
    spot = spot_costs(manifest)
    rows, source, quality = load_rows(manifest, start, end)
    if not rows or rows[0][0] > start + timedelta(days=7) or rows[-1][0] < end - timedelta(days=8):
        raise ValueError("Data does not cover the requested research period")
    config = dict(start=start, end=end, symbol=manifest["data"]["symbol"], paths=paths, seed=seed,
                  shock_bps=shock_bps, strategy=manifest["id"], levels=manifest["levels"],
                  calendar=manifest["calendar"])
    folds = harness.study(rows, Plugin(manifest), manifest["levels"], paths, shock_bps, seed, start, end,
                          StressConfig(), spot, short_rate(manifest), mc, manifest.get("walk_forward"))
    return dict(config=config, manifest=manifest, data_sha256=hashlib.sha256(repr(rows).encode()).hexdigest(),
                execution_contract=dict(engine_sha256=harness.engine_digest(),
                                        fee_profile=spot.profile if spot else harness.FEE_PROFILE,
                                        starting_cash=START_CASH),
                currency="USD", source=source, data_quality=quality, folds=folds,
                abstentions=sum(f["abstentions"] for f in folds))


def run_replay(manifest, start, end, level):
    spot = spot_costs(manifest)
    rows, _, _ = load_rows(manifest, start - timedelta(days=2 * manifest["warmup"] + 10), end)
    prior = [r for r in rows if r[0] < start]
    window = [r for r in rows if start <= r[0] < end]
    if not window or len(prior) < manifest["warmup"]:
        raise ValueError("Data does not cover the warmup and the requested range")
    plugin = Plugin(manifest)
    fit = getattr(plugin, "fit", None)
    if fit and not prior:
        raise ValueError("A fitted strategy needs history before --start to fit on")
    parameter = fit(tuple(prior), level) if fit else level
    log = {"abstentions": 0}
    (_, shares), equity, fills = harness.replay(window, plugin, parameter, (START_CASH, 0),
                                                [r[2] for r in prior], spot=spot, log=log,
                                                short=short_rate(manifest))
    return dict(id=manifest["id"], start=start, end=end, level=level, ending_equity=equity[-1],
                ending_shares=shares, sessions=len(window), fills=fills, abstentions=log["abstentions"])


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["mc"]:  # Monte Carlo risk run for any engine; see mc_runs.py
        import mc_runs
        return mc_runs.main(argv[1:])
    if argv[:1] == ["xs"]:  # cross-sectional runs have their own manifest schema; see xsection.py
        import xsection
        return xsection.main(argv[1:])
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("test", "replay"):
        p = sub.add_parser(name)
        p.add_argument("manifest", type=Path)
        p.add_argument("--start", type=date.fromisoformat, default=date(2022, 1, 1))
        p.add_argument("--end", type=date.fromisoformat, default=date(2024, 1, 1), help="Exclusive")
        p.add_argument("--out", type=Path)
        if name == "test":
            p.add_argument("--paths", type=int, default=20)
            p.add_argument("--shock-bps", type=float, default=10.)
            p.add_argument("--seed", type=int, default=42)
        else:
            p.add_argument("--level", type=float, help="Defaults to the first manifest level")
    p = sub.add_parser("compare")
    p.add_argument("left", type=Path)
    p.add_argument("right", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "compare":
            reports = [json.loads(f.read_text(encoding="utf-8")) for f in (args.left, args.right)]
            print(json.dumps(compare_reports.compare(*reports), indent=2, allow_nan=False))
            return
        manifest = load_manifest(args.manifest)
        if args.command == "test":
            result = run_test(manifest, args.start, args.end, args.paths, args.shock_bps, args.seed)
            out = args.out or Path("reports") / f"{manifest['id']}.json"
        else:
            level = manifest["levels"][0] if args.level is None else args.level
            result = run_replay(manifest, args.start, args.end, level)
            out = args.out
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        parser.exit(2, f"{args.command} failed: {exc}\n")
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    if args.command == "test":
        for f in result["folds"]:
            print(f"{f['forward_start']}..{f['end_exclusive']} selected={f['selected']} "
                  f"forward_return={f['forward_return']:.4%} fills={len(f['fills'])} abstentions={f['abstentions']}")
        print(f"report: {out}  abstentions={result['abstentions']}")
    else:
        print(json.dumps(dict(result, fills=len(result["fills"])), indent=2, default=str))


if __name__ == "__main__":
    main()

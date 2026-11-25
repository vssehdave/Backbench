"""Monte Carlo risk runs: python money.py mc <manifest> [--paths 1000 --seed 0]. See docs/monte-carlo.md.

The manifest picks the engine: a "cadence" field is a cross-section manifest (mode A on the panel), a "runner" of
options_bt.py is an option strategy (mode B), anything else is the single-instrument harness (mode A on bars).
"""
import argparse
import json
import time
from datetime import date, timedelta
from pathlib import Path

import montecarlo
import report

BENCHMARK = Path(__file__).parent / "strategies" / "catalog" / "_benchmarks" / "buy_and_hold_spy.json"


def out_dir(manifest_path, engine):
    """(results folder, mc_results file) beside the manifest. A variant (manifest_long_short.json, or any xs
    manifest) gets its own results/<variant>/ folder and mc_results_<variant>.json."""
    path = Path(manifest_path)
    variant = path.stem if engine == "xsection" else path.stem.removeprefix("options_manifest").removeprefix(
        "manifest").strip("_")
    base = path.parent / "results"
    return (base / variant if variant else base), path.parent / f"mc_results{'_' + variant if variant else ''}.json"


def finish(folder, engine, name, result, folds, runs, config, started, seed, extra=None, spy=None):
    """runs is {label: montecarlo summary}. Writes report.json, REPORT.md, trade logs and the mc_results file."""
    folder, target = folder
    seconds = time.perf_counter() - started
    config = dict(config, runtime_seconds=round(seconds, 1))
    report.write_report(folder, engine, name, result, runs, folds, seed, dict(mc_config=config, **(extra or {})), spy)
    target.write_text(json.dumps(dict(name=name, config=config, series=runs), indent=2), encoding="utf-8")
    print(f"{name}: {seconds:.0f}s, wrote {folder} and {target}")
    return target


def run_single(manifest_path, start, end, paths, seed, block, stress_paths):
    import money
    started = time.perf_counter()
    manifest = money.load_manifest(manifest_path)
    bench = money.load_manifest(BENCHMARK)
    mcs = {k: montecarlo.MonteCarlo(paths, seed, block) for k in ("strategy", "benchmark")}
    results = {k: money.run_test(m, start, end, stress_paths, 10., seed,
                                 lambda *a, k=k: mcs[k].rows_fold(k, *a))
               for k, m in (("strategy", manifest), ("benchmark", bench))}
    runs = {k: mcs[k].summary()["mode_a"][k] for k in mcs}
    # The walk-forward windows (July-December) skip Q1 2020, so also show the whole-period benchmark, bootstrapped as mode B.
    full = [r[2] / mcs["benchmark"].rows[0][2] for r in mcs["benchmark"].rows if start <= r[0] < end]
    runs["benchmark full history (mode B)"] = montecarlo.pnl_bootstrap(
        {"b": full}, paths, seed, block)["b"]
    folds = report.folds_of("harness", results["strategy"], results["benchmark"])
    config = dict(note="Max drawdown is on the continuous backtest from start to end (or, with walk_forward, the contiguous test "
                       "windows chained into one equity curve per path).",
                  mode="A: path rerun on bootstrapped bars", paths=paths, seed=seed, mean_block=block, start=str(start),
                  end=str(end), stress_paths=stress_paths)
    return finish(out_dir(manifest_path, "harness"), "harness", manifest["id"], results["strategy"], folds, runs,
                  config, started, seed, dict(benchmark_result=results["benchmark"]))


def run_xs(manifest_path, start, end, paths, seed, block):
    import xs_data
    import xsection
    started = time.perf_counter()
    hook = json.loads(Path(manifest_path).read_text(encoding="utf-8")).get("panel")
    if hook:  # "module:function" beside the manifest, for strategies on their own universe (FAA's ETFs)
        import importlib, sys
        sys.path.insert(0, str(Path(manifest_path).resolve().parent))
        mod, fn = hook.split(":")
        panel = getattr(importlib.import_module(mod), fn)(date(2015, 1, 1), end)
    else:
        panel = xs_data.build_panel(date(2015, 1, 1), end)
    mc = montecarlo.MonteCarlo(paths, seed, block)
    result = xsection.run(manifest_path, start, end, panel, mc=mc.panel_fold)
    summary = mc.summary()
    runs = dict(summary["mode_a"], **{"benchmark (SPY)": summary["mode_a"].pop("spy")}) if "spy" in summary["mode_a"] \
        else summary["mode_a"]
    runs.pop("spy", None)
    folds = report.folds_of("xsection", result)
    config = dict(note="Max drawdown is on the continuous backtest (or, with walk_forward, the contiguous test windows "
                       "chained into one equity curve per path).",
                  mode="A: path rerun on jointly bootstrapped dates", paths=paths, seed=seed, mean_block=block,
                  start=str(start), end=str(end))
    return finish(out_dir(manifest_path, "xsection"), "xsection", result["manifest"]["id"], result, folds, runs, config,
                  started, seed)


def run_options(manifest_path, paths, seed, block):
    import options_bt as ob
    import options_data as od
    started = time.perf_counter()
    m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    today, start = date.today(), date.fromisoformat(m["start"])
    closes = od.underlying_closes(m["data"]["underlying"], start, today - timedelta(days=1))
    expiries = ob.monthly_expiries(set(closes), start, today - timedelta(days=1))
    contracts = lambda e, k, lo, hi: od.contracts(m["data"]["underlying"], e, k, lo, hi, today)
    result = ob.run(m["strategy"], closes, expiries, contracts, od.option_closes, capital=m["capital"],
                    half_spread=m["half_spread_per_share"]["value"], fee=m["fee_per_contract"])
    daily = result["daily"]
    both = montecarlo.pnl_bootstrap(dict(strategy=daily["equity"], benchmark=daily["buy_and_hold"]), paths, seed, block)
    runs = both
    config = dict(mode="B: block bootstrap of the strategy's own daily equity returns", paths=paths, seed=seed,
                  mean_block=block, start=str(daily["dates"][0]), end=str(daily["dates"][-1]))
    return finish(out_dir(manifest_path, "options"), "options", m["id"], result, report.folds_of("options", result),
                  runs, config, started, seed,
                  spy=closes if m["data"]["underlying"] == "SPY" else od.underlying_closes("SPY", start, today - timedelta(days=1)))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--paths", type=int, default=None, help="default 1000; 200 for cross-section manifests")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--block", type=float, default=20., help="mean block length in sessions")
    parser.add_argument("--start", type=date.fromisoformat, default=date(2016, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date(2026, 1, 1), help="Exclusive")
    parser.add_argument("--stress-paths", type=int, default=20, help="existing execution-stress paths (single instrument)")
    args = parser.parse_args(argv)
    m = json.loads(args.manifest.read_text(encoding="utf-8"))
    if "cadence" in m:
        run_xs(args.manifest, args.start, date(2026, 11, 1) if args.end == date(2026, 1, 1) else args.end,
               args.paths or 200, args.seed, args.block)
    elif m.get("runner") == "options_bt.py":
        run_options(args.manifest, args.paths or 1000, args.seed, args.block)
    else:
        run_single(args.manifest, args.start, args.end, args.paths or 1000, args.seed, args.block, args.stress_paths)


if __name__ == "__main__":
    main()

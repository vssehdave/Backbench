"""Cross-sectional long/short walk-forward engine. Run with python xsection.py --help. See docs/cross-section.md."""
import argparse
import hashlib
import importlib
import json
import math
import re
import statistics
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from harness import months_after

FEE_PROFILE = "ibkr-tiered-like-2026-11-23"
MANIFEST_FIELDS = {"id", "version", "entry", "cadence", "levels", "limits", "benchmark"}
LIMIT_FIELDS = {"max_gross", "max_net", "name_cap"}


@dataclass(frozen=True)
class Costs:
    commission_per_share: float = 0.0035
    commission_min: float = 0.35
    commission_max_pct: float = 0.01
    slippage_bps: float = 5.
    borrow_bps: float = 50.  # annual, general collateral
    sell_fee_pct: float = 0.0000206  # sell-side regulatory estimate, as in harness.fees
    sell_fee_per_share: float = 0.000003
    margin_bps: float = 0.  # annual interest on negative cash (leverage), booked under "borrow"; 0 keeps old runs unchanged


@dataclass(frozen=True)
class Limits:
    max_gross: float
    max_net: float
    name_cap: float


@dataclass(frozen=True)
class AsOf:
    """Everything a strategy may see at a decision: adjusted closes up to and including `date`, nothing later."""
    date: date
    dates: tuple
    prices: dict  # symbol -> tuple of adjusted closes aligned to dates, None before a bar exists
    aux: dict = field(default_factory=dict)  # reference series (factor ETFs): visible, truncated, never tradable


def enforce(weights, limits):
    """Per-name cap, then net, then gross limit. Returns a new dict; the strategy's own is untouched."""
    if not all(math.isfinite(x) for x in weights.values()):
        raise ValueError("Strategy returned a non-finite weight")
    w = {s: max(-limits.name_cap, min(limits.name_cap, x)) for s, x in weights.items() if x}
    long_, short = sum(x for x in w.values() if x > 0), -sum(x for x in w.values() if x < 0)
    if long_ - short > limits.max_net + 1e-12 and long_:
        k = (short + limits.max_net) / long_
        w = {s: x * k if x > 0 else x for s, x in w.items()}
    elif short - long_ > limits.max_net + 1e-12 and short:
        k = (long_ + limits.max_net) / short
        w = {s: x * k if x < 0 else x for s, x in w.items()}
    gross = sum(abs(x) for x in w.values())
    if gross > limits.max_gross + 1e-12:
        w = {s: x * limits.max_gross / gross for s, x in w.items()}
    return {s: x for s, x in w.items() if abs(x) > 1e-15}


def trade_costs(value, raw_price, costs):
    """(commission, regulatory, slippage) in USD for one trade of signed USD value (negative = sell/short)."""
    size = abs(value)
    shares = size / raw_price
    commission = min(max(costs.commission_min, shares * costs.commission_per_share), size * costs.commission_max_pct)
    regulatory = shares * costs.sell_fee_per_share + (size * costs.sell_fee_pct if value < 0 else 0)
    return commission, regulatory, size * costs.slippage_bps / 10000


def decision_indexes(dates, i0, i1, cadence):
    """Sessions whose close starts a decision: the baseline plus the last session of each month or ISO week (or every session)."""
    if cadence == "daily":
        return list(range(i0, i1))
    key = (lambda d: (d.year, d.month)) if cadence == "monthly" else (lambda d: d.isocalendar()[:2])
    return [i0] + [i for i in range(i0 + 1, i1) if key(dates[i + 1]) != key(dates[i])]


def view(panel, i):
    """The as-of panel: members on dates[i] that have a bar that day, history truncated at i."""
    members = panel.members[i] if panel.members else panel.adj.keys()
    prices = {s: tuple(panel.adj[s][:i + 1]) for s in sorted(members) if s in panel.adj and panel.adj[s][i] is not None}
    aux = {s: tuple(v[:i + 1]) for s, v in sorted(getattr(panel, "aux", {}).items())}
    return AsOf(panel.dates[i], tuple(panel.dates[:i + 1]), prices, aux)


def run_window(panel, decide, params, i0, i1, limits, costs, cadence, cash0):
    """Hold cash at close i0, decide at each decision close, trade at the next session's close, mark daily to i1.

    Positions are held in adjusted-price units (dividends are reinvested through the adjusted return). Raw prices
    only convert traded value to a share count for commissions.
    """
    cash, units, last = cash0, {}, {}
    equity, long_pnl, short_pnl = [cash0], 0., 0.
    paid = dict(commission=0., regulatory=0., slippage=0., borrow=0.)
    traded, forced, abstain, log, pending = 0., 0, 0, [], None
    decisions = set(decision_indexes(panel.dates, i0, i1, cadence))

    def charge(symbol, value, k):
        nonlocal cash, traded
        c, r, s = trade_costs(value, panel.raw[symbol][k], costs)
        for name, amount in zip(("commission", "regulatory", "slippage"), (c, r, s)):
            paid[name] += amount
        cash -= value + c + r + s
        traded += abs(value)

    for k in range(i0, i1 + 1):
        if k > i0:
            gap = (panel.dates[k] - panel.dates[k - 1]).days
            for s in list(units):
                price = panel.adj[s][k]
                if price is None and panel.last[s] < k:
                    # Delisted: close at the last price seen, with trading costs.
                    price = last[s]
                    charge(s, -units[s] * price, panel.last[s])
                    del units[s]
                    forced += 1
                    continue
                price = last[s] if price is None else price  # temporary gap: carry the last price
                pnl = units[s] * (price - last[s])
                long_pnl, short_pnl = (long_pnl + pnl, short_pnl) if units[s] > 0 else (long_pnl, short_pnl + pnl)
                fee = 0 if units[s] > 0 else -units[s] * last[s] * costs.borrow_bps / 10000 * gap / 365
                cash -= fee
                paid["borrow"] += fee
                last[s] = price
            if cash < 0 and costs.margin_bps:
                fee = -cash * costs.margin_bps / 10000 * gap / 365
                cash -= fee
                paid["borrow"] += fee
            if pending is not None:
                value = cash + sum(units[s] * last[s] for s in units)
                for s in sorted(set(units) | set(pending)):
                    if panel.adj[s][k] is None:
                        continue  # no bar on the fill day: leave the position as it is
                    delta = pending.get(s, 0.) * value - units.get(s, 0.) * panel.adj[s][k]
                    if delta:
                        charge(s, delta, k)
                        units[s] = units.get(s, 0.) + delta / panel.adj[s][k]
                        last[s] = panel.adj[s][k]
                        if abs(units[s]) < 1e-12:
                            del units[s]
                pending = None
            equity.append(cash + sum(units[s] * last[s] for s in units))
        if k in decisions and k < i1:
            seen = view(panel, k)
            target = decide(seen, params)
            if target is None:
                abstain += 1
            else:
                unknown = set(target) - set(seen.prices)
                if unknown:
                    raise ValueError(f"{panel.dates[k]}: weights for symbols outside the as-of universe: "
                                     f"{sorted(unknown)[:5]}")
                pending = enforce(target, limits)
                log.append((str(panel.dates[k]), dict(sorted(pending.items()))))
    return dict(equity=equity, long_pnl=long_pnl, short_pnl=short_pnl, costs=paid, traded=traded,
                forced_closes=forced, abstentions=abstain, decisions=log, cash=cash, units=units)


def _benchmark(panel, symbols, i0, i1, cash0):
    """Buy and hold with no costs. A name with no later bar stays at its last price; no reinvestment."""
    units = {s: cash0 / len(symbols) / panel.adj[s][i0] for s in symbols}
    out, last = [], {s: panel.adj[s][i0] for s in symbols}
    for k in range(i0, i1 + 1):
        for s in symbols:
            last[s] = panel.adj[s][k] if panel.adj[s][k] is not None else last[s]
        out.append(sum(units[s] * last[s] for s in symbols))
    return out


def stats(equity):
    returns = [b / a - 1 for a, b in zip(equity, equity[1:])]
    sd = statistics.stdev(returns) if len(returns) > 1 else 0.
    peak, drawdown = equity[0], 0.
    for e in equity:
        peak = max(peak, e)
        drawdown = min(drawdown, e / peak - 1)
    return dict(total_return=equity[-1] / equity[0] - 1, volatility=sd * math.sqrt(252),
                sharpe=statistics.fmean(returns) / sd * math.sqrt(252) if sd else None, max_drawdown=drawdown)


def folds(start, end):
    """Same schedule as harness.study: 6-month selection, 6-month test, 12-month steps."""
    while months_after(start, 12) <= end:
        split = months_after(start, 6)
        stop = months_after(split, 6)
        yield start, split, stop
        start = stop


def _first(dates, day):
    for i, d in enumerate(dates):
        if d >= day:
            return i
    raise ValueError(f"Panel ends before {day}")


def study(panel, strategy, levels, limits, costs, cadence, start, end, cash0=1_000_000., benchmark="SPY"):
    """strategy is a (decide, fit-or-None) pair. Each fold starts from cash0 on its own."""
    decide, fit = strategy
    results = []
    for train, split, stop in folds(start, end):
        i_train, i_split, i_stop = _first(panel.dates, train), _first(panel.dates, split), _first(panel.dates, stop)
        i_train = max(i_train, 1)  # the panel can start inside the first fold; the baseline needs one session before
        i_inner = _first(panel.dates, months_after(train, 3)) if fit else i_train
        scores = {}
        for n, level in enumerate(levels):
            artifact = fit(view(panel, i_inner - 1), level) if fit else level
            run = run_window(panel, decide, artifact, i_inner - 1, i_split - 1, limits, costs, cadence, cash0)
            scores[n] = stats(run["equity"])["sharpe"]
        best = max(scores, key=lambda n: (scores[n] is not None, scores[n] or 0, -n))
        artifact = fit(view(panel, i_split - 1), levels[best]) if fit else levels[best]
        run = run_window(panel, decide, artifact, i_split - 1, i_stop - 1, limits, costs, cadence, cash0)
        years = (panel.dates[i_stop - 1] - panel.dates[i_split - 1]).days / 365
        spent = sum(run["costs"].values())
        members = [s for s in view(panel, i_split - 1).prices]
        bench = dict(equal_weight_universe=_benchmark(panel, members, i_split - 1, i_stop - 1, cash0),
                     cash=[cash0] * (i_stop - i_split + 1))
        if benchmark in panel.adj and panel.adj[benchmark][i_split - 1] is not None:
            bench["spy"] = _benchmark(panel, [benchmark], i_split - 1, i_stop - 1, cash0)
        results.append(dict(
            selection_start=str(panel.dates[i_inner]), test_start=str(panel.dates[i_split]),
            test_end=str(panel.dates[i_stop - 1]), selected_level=levels[best], selection_sharpe=scores,
            strategy=stats(run["equity"]), benchmarks={k: stats(v) for k, v in bench.items()},
            turnover_per_year=run["traded"] / cash0 / years, cost_drag=spent / cash0,
            costs_usd=run["costs"], long_leg_return=run["long_pnl"] / cash0, short_leg_return=run["short_pnl"] / cash0,
            decisions=len(run["decisions"]), abstentions=run["abstentions"], forced_closes=run["forced_closes"],
            names_held_avg=statistics.fmean(len(w) for _, w in run["decisions"]) if run["decisions"] else 0,
            equity=run["equity"], bench_equity=bench, decision_log=run["decisions"]))
    if not results:
        raise ValueError("Supply at least twelve complete calendar months")
    return results


def load_manifest(path):
    """Validate an xs manifest and return it with the strategy callables; raise one error listing every problem."""
    path = Path(path)
    m = json.loads(path.read_text(encoding="utf-8"))
    errors = [f"missing field: {k}" for k in sorted(MANIFEST_FIELDS - m.keys())]
    errors += [f"unknown field: {k}" for k in sorted(m.keys() - MANIFEST_FIELDS)]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", str(m.get("id", ""))):
        errors.append("id may only contain letters, digits, '_', '.' and '-'")
    if m.get("cadence") not in ("monthly", "weekly"):
        errors.append("cadence must be 'monthly' or 'weekly'")
    if not (isinstance(m.get("levels"), list) and m["levels"] and all(isinstance(x, dict) for x in m["levels"])):
        errors.append("levels must be a non-empty list of parameter objects")
    limits = m.get("limits")
    if not (isinstance(limits, dict) and set(limits) == LIMIT_FIELDS
            and all(type(v) in (int, float) and math.isfinite(v) and v >= 0 for v in limits.values())
            and limits["max_gross"] > 0 and limits["name_cap"] > 0):
        errors.append("limits must give finite non-negative max_gross, max_net and name_cap (gross and cap above 0)")
    strategy = None
    if isinstance(m.get("entry"), str) and re.fullmatch(r"[\w.]+:\w+", m["entry"]):
        folder = str(path.resolve().parent)
        name = m["entry"].split(":")[0]
        # Folders may reuse one module name (strategy_xs): put this one first and drop another folder's cached copy.
        if folder in sys.path:
            sys.path.remove(folder)
        sys.path.insert(0, folder)
        cached = getattr(sys.modules.get(name), "__file__", None)
        if cached and Path(cached).resolve().parent != Path(folder):
            del sys.modules[name]
        try:
            module = importlib.import_module(name)
            decide = getattr(module, m["entry"].split(":")[1])
            fit = getattr(module, "fit", None)
            strategy = (decide, fit)
        except (ImportError, AttributeError) as exc:
            errors.append(f"entry {m['entry']} cannot be imported: {exc}")
    else:
        errors.append("entry must look like 'module:name'")
    if errors:
        raise ValueError(f"Invalid manifest {path}:\n" + "\n".join(f"  - {e}" for e in errors))
    return m, strategy


def run(manifest_path, start, end, panel, costs=Costs(), cash0=1_000_000.):
    m, strategy = load_manifest(manifest_path)
    limits = Limits(**m["limits"])
    fold_results = study(panel, strategy, m["levels"], limits, costs, m["cadence"], start, end, cash0, m["benchmark"])
    first, last = _first(panel.dates, start), max(i for i, d in enumerate(panel.dates) if d < end)
    survivorship = None
    if panel.members:
        from xs_data import coverage
        survivorship = coverage(panel, first, last)
    return dict(manifest=m, config=dict(start=start, end=end, start_cash=cash0, costs=asdict(costs),
                                        fee_profile=FEE_PROFILE),
                data=dict(quality=panel.quality, survivorship=survivorship,
                          panel_sha256=hashlib.sha256(repr((panel.dates, sorted(panel.adj.items()))).encode()).hexdigest()),
                folds=fold_results)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--start", type=date.fromisoformat, default=date(2016, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date(2026, 11, 1), help="Exclusive")
    parser.add_argument("--fetch-from", type=date.fromisoformat, default=date(2015, 1, 1), help="Warm-up history start")
    parser.add_argument("--borrow-bps", type=float, default=Costs.borrow_bps)
    parser.add_argument("--slippage-bps", type=float, default=Costs.slippage_bps)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    import xs_data
    try:
        panel = xs_data.build_panel(args.fetch_from, args.end, log=print)
        report = run(args.manifest, args.start, args.end, panel,
                     Costs(borrow_bps=args.borrow_bps, slippage_bps=args.slippage_bps))
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        parser.exit(2, f"xs run failed: {exc}\n")
    out = args.out or Path("reports") / f"xs_{report['manifest']['id']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    for f in report["folds"]:
        s, e, c = f["strategy"], f["benchmarks"]["equal_weight_universe"], f["benchmarks"].get("spy", {})
        print(f"{f['test_start']}..{f['test_end']} ret={s['total_return']:.2%} sharpe={s['sharpe']} "
              f"ew={e['total_return']:.2%} spy={c.get('total_return', float('nan')):.2%} abst={f['abstentions']}")
    print(f"report: {out}")


if __name__ == "__main__":
    main()

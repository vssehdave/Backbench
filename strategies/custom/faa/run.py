"""Run every FAA model the paper reports over 2016-2026 on the ETF proxies. Usage: python strategies/custom/faa/run.py"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(Path(__file__).parent)]
import customlib
import faa_rules
import xs_data
import xsection

UNLEVERED = xsection.Limits(1., 1., 1.)
# Paper par. 12: lev=2, 3% a year on the borrowed half, tc=0.1% per transaction (modelled as 10 bps slippage, no commission).
LEVERED = xsection.Limits(2., 2., 2.)  # name cap 2: all three slots can land in SHY
PAPER_LEV_COSTS = xsection.Costs(commission_per_share=0., commission_min=0., slippage_bps=10., margin_bps=300.)
RAVC = dict(w_return=1., w_volatility=.5, w_correlation=.5)
FITTED = dict(w_return=1., w_volatility=.8, w_correlation=.6)
# The paper's ladder, in its order, plus the old 84-session run kept to confirm the earlier result.
LADDER = [
    ("ew7", "Benchmark: equal weight 7, monthly rebalance", None, {}),
    ("r", "R only (top 3, no cash rule)", dict(w_return=1., w_volatility=0., w_correlation=0., abs_filter=False), {}),
    ("ra", "R + A", dict(w_return=1., w_volatility=0., w_correlation=0.), {}),
    ("rav", "R, A, V 100/50/0", dict(w_return=1., w_volatility=.5, w_correlation=0.), {}),
    ("ravc", "R, A, V, C 100/50/50 (default)", RAVC, {}),
    ("ravc_84", "R, A, V, C 100/50/50, 84-session lookback (previous run)", dict(RAVC, lookback=84), {}),
    ("ravc_fitted", "R, A, V, C 100/80/60 (fitted by the authors on 2005-12)", FITTED, {}),
    ("ravc_fitted_lev2", "R, A, V, C 100/80/60, lev 2, 3% interest, tc 0.1%", dict(FITTED, leverage=2.),
     dict(limits=LEVERED, costs=PAPER_LEV_COSTS)),
    ("ravc_log", "R, A, V, C 100/50/50, log loss (eq. 3)", dict(RAVC, form="log"), {}),
]


def etf_panel(start, end, log=print):
    symbols = sorted(set(faa_rules.UNIVERSE) | {"SPY"})
    spy = xs_data.fetch_bars(["SPY"], start, end, "all")["SPY"]
    dates = [date.fromisoformat(d) for d, _ in spy]
    index = {d: i for i, d in enumerate(dates)}
    adj_rows, raw_rows = (xs_data.fetch_bars(symbols, start, end, k, data_dir=ROOT / "data/alpaca_xs") for k in ("all", "raw"))
    adj, raw = {}, {}
    for s in symbols:
        for rows, out in ((adj_rows[s], adj), (raw_rows[s], raw)):
            by = {date.fromisoformat(d): c for d, c in rows}
            out[s] = [by.get(d) for d in dates]
    return xs_data.Panel(dates, adj, raw, None, dict(symbols=symbols, sessions=len(dates)))


def equal_weight(seen, _):
    return {s: 1 / len(faa_rules.UNIVERSE) for s in faa_rules.UNIVERSE}


def run_variant(panel, params, start, limits=UNLEVERED, costs=xsection.Costs()):
    decide = equal_weight if params is None else (lambda seen, _: faa_rules.decide(seen, params))
    return customlib.run_panel(panel, decide, limits, "monthly", start, costs=costs)


def row(r):
    m = r["metrics"]
    return dict(cagr=m["cagr"], volatility=m["volatility"], sharpe=m["sharpe"], max_drawdown=m["max_drawdown"],
                turnover_per_year=r["turnover_per_year"], costs_pct_of_avg_equity_per_year=r["costs_pct_of_avg_equity_per_year"])


def log_vs_rank(panel, decisions):
    """Months where eq. 3 and the rank form pick a different top 3, and where the final weights differ."""
    sets = weights = 0
    for day, _ in decisions:
        seen = xsection.view(panel, panel.dates.index(date.fromisoformat(day)))
        f = faa_rules.factors(seen, {**faa_rules.DEFAULTS, **RAVC})
        if f is None:
            continue
        p = {**faa_rules.DEFAULTS, **RAVC}
        sets += set(faa_rules.picks(*f, p)) != set(faa_rules.picks(*f, dict(p, form="log")))
        weights += faa_rules.decide(seen, RAVC) != faa_rules.decide(seen, dict(RAVC, form="log"))
    return dict(months=len(decisions), top3_set_differs=sets, final_weights_differ=weights)


def main():
    panel = etf_panel(date(2015, 1, 1), date(2026, 11, 1))
    start = date(2016, 6, 1)  # ETF bars start 2016-01-04 (Alpaca); January's month-end is the first 4-month anchor
    variants, ladder_runs = {}, {}
    for key, label, params, extra in LADDER:
        r = run_variant(panel, params, start, **extra)
        ladder_runs[key] = r
        variants[key] = dict(label=label, params=params, **row(r), costs_usd=r["costs_usd"], period=[r["metrics"]["start"], r["metrics"]["end"]],
                             decisions=r["decisions"], abstentions=r["abstentions"], decision_log=r["decision_log"])
    # Sensitivity, not selection: common start where a 6-month lookback exists (July 2016 month-end).
    grid_start = date(2016, 8, 1)
    sensitivity = {}
    for n in (2, 3, 4):
        for months in (3, 4, 6):
            r = run_variant(panel, dict(RAVC, n=n, lookback_months=months), grid_start)
            sensitivity[f"N{n}_{months}m"] = dict(n=n, lookback_months=months, period=[r["metrics"]["start"], r["metrics"]["end"]],
                                                  **row(r))
    i0 = max(customlib.first_index(panel, start) - 1, 0)
    bench = {"SPY_buy_hold_total_return": customlib.buy_hold(panel, "SPY", i0, len(panel.dates) - 1)}
    ew = [sum(panel.adj[s][i] / panel.adj[s][i0] for s in faa_rules.UNIVERSE) / 7 for i in range(i0, len(panel.dates))]
    bench["equal_weight_7_buy_hold_no_rebalance"] = customlib.metrics(panel.dates[i0:], ew)
    out = dict(strategy="FAA, all models in Keller and van Putten (2012)", universe=faa_rules.UNIVERSE, cash=faa_rules.CASH,
               defaults=faa_rules.DEFAULTS, costs=dict(profile=xsection.FEE_PROFILE, **vars(xsection.Costs())),
               lev2_costs=vars(PAPER_LEV_COSTS), variants=variants, log_vs_rank=log_vs_rank(panel, ladder_runs["ravc"]["decision_log"]),
               sensitivity=dict(note="Sensitivity only, not used to pick parameters. RAVC 100/50/50.", start=str(grid_start),
                                runs=sensitivity),
               benchmarks=bench, equity_every_21_sessions=ladder_runs["ravc"]["equity"][::21])
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    pct = lambda x: f"{x:.1%}"
    for name, rows in (("ladder", {k: v for k, v in variants.items()}), ("sensitivity", sensitivity)):
        print(name)
        for k, v in rows.items():
            print(f"  {k:18} cagr={pct(v['cagr'])} vol={pct(v['volatility'])} sharpe={v['sharpe']:.2f} "
                  f"dd={pct(v['max_drawdown'])} turn={v['turnover_per_year']:.1f}x cost={v['costs_pct_of_avg_equity_per_year']:.2%}")
    print("log_vs_rank", out["log_vs_rank"])
    print("SPY", {k: round(v, 3) for k, v in bench["SPY_buy_hold_total_return"].items() if k in ("cagr", "max_drawdown")})


if __name__ == "__main__":
    main()

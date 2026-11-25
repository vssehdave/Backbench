"""Munger 200-week MA on the S&P 500 point-in-time panel. Usage: python strategies/custom/munger-200wma/run.py (needs fetch_edgar.py)."""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(Path(__file__).parent)]
import customlib
import edgar
import munger_rules
import xs_data
import xsection


def equal_weight(seen, params):
    return {s: 1 / len(seen.prices) for s in seen.prices}


def main():
    panel = xs_data.build_panel(date(2015, 1, 1), date(2026, 11, 1))
    ciks = edgar.ticker_map(ROOT / "data/edgar")
    records = {s: r for s in panel.adj if s in ciks and (r := edgar.company(ciks[s], ROOT / "data/edgar"))}
    limits = xsection.Limits(1., 1., 1.)
    # First session with 200 weekly closes for the benchmarks' common window.
    probe = next(i for i in range(len(panel.dates)) if munger_rules.weekly_ma(panel.dates[:i + 1], panel.adj["AAPL"][:i + 1]))
    start = panel.dates[probe]
    run = customlib.run_panel(panel, munger_rules.make_decide(records), limits, "monthly", start)
    ew = customlib.run_panel(panel, equal_weight, limits, "monthly", start)
    i0 = customlib.first_index(panel, start) - 1
    passing = {}
    for i in range(probe, len(panel.dates), 63):
        d = panel.dates[i]
        names = [s for s in panel.members[i] if s in records and panel.adj[s][i] is not None]
        passing[str(d)] = dict(members=len(panel.members[i]), with_edgar=len(names),
                               quality=sum(munger_rules.high_quality(records[s], d) for s in names))
    out = dict(strategy=f"Munger 200-week MA, quality screen, exit {munger_rules.EXIT_ABOVE:.0%} above MA, monthly, equal weight",
               window_start=str(start), result={k: v for k, v in run.items() if k not in ("equity", "dates", "decision_log")},
               holdings_each_month=[(d, len(w)) for d, w in run["decision_log"]], quality_pass_counts=passing,
               benchmarks=dict(SPY_buy_hold_total_return=customlib.buy_hold(panel, "SPY", i0, len(panel.dates) - 1),
                               equal_weight_sp500_monthly=ew["metrics"], equal_weight_turnover_per_year=ew["turnover_per_year"],
                               cash=dict(cagr=0., volatility=0., sharpe=None, max_drawdown=0.)),
               coverage=dict(symbols_in_panel=len(panel.adj), with_edgar=len(records)))
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(run["metrics"], run["turnover_per_year"], run["costs_pct_of_avg_equity_per_year"], run["names_held_avg"])
    print("SPY", out["benchmarks"]["SPY_buy_hold_total_return"])
    print("EW", ew["metrics"])
    print(passing)
    customlib.report_panel(Path(__file__).parent, "munger-200wma", panel, lambda p: munger_rules.make_decide(records), limits,
                           "monthly", start)


if __name__ == "__main__":
    main()

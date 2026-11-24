"""Run FAA over 2016-2026 on the ETF proxies. Usage: python strategies/custom/faa/run.py"""
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


def main():
    panel = etf_panel(date(2015, 1, 1), date(2026, 11, 1))
    limits = xsection.Limits(1., 1., 1.)
    start = date(2016, 6, 1)  # ETF bars start 2016-01-04 (Alpaca), so 84 sessions of history exist only from 2016-05-31
    r = customlib.run_panel(panel, faa_rules.decide, limits, "monthly", start)
    i0 = max(customlib.first_index(panel, start) - 1, 0)
    first_trade = next((d for d, _ in r["decision_log"]), None)
    bench = {"SPY_buy_hold_total_return": customlib.buy_hold(panel, "SPY", i0, len(panel.dates) - 1),
             "equal_weight_7_buy_hold": None,
             "cash": dict(cagr=0., volatility=0., sharpe=None, max_drawdown=0.)}
    ew = [sum(panel.adj[s][i] / panel.adj[s][i0] for s in faa_rules.UNIVERSE) / 7 for i in range(i0, len(panel.dates))]
    bench["equal_weight_7_buy_hold"] = customlib.metrics(panel.dates[i0:], ew)
    out = dict(strategy="FAA (RAVC, N=3 of 7, 4m, weights 100/50/50)", universe=faa_rules.UNIVERSE, cash=faa_rules.CASH,
               parameters=dict(lookback_sessions=faa_rules.LOOKBACK, n=3, wR=1, wV=.5, wC=.5, tuned=False),
               costs=dict(profile=xsection.FEE_PROFILE, **vars(xsection.Costs())), result={k: v for k, v in r.items()
                          if k not in ("equity", "dates")}, benchmarks=bench, first_decision=first_trade,
               equity_every_21_sessions=r["equity"][::21])
    # results.json is committed: keep the decision log (monthly) and drop the daily curve.
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    m = r["metrics"]
    print(json.dumps(dict(strategy=m, turnover=r["turnover_per_year"], cost_pct=r["costs_pct_of_avg_equity_per_year"],
                          **{k: {x: y for x, y in v.items() if x in ("cagr", "volatility", "sharpe", "max_drawdown")}
                             for k, v in bench.items()}), indent=1, default=str))


if __name__ == "__main__":
    main()

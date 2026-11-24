"""Hold the largest S&P 500 member. Usage: python strategies/custom/sp500-top-holding/run.py (needs fetch_edgar.py first)."""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(Path(__file__).parent)]
import customlib
import edgar
import leader_rules
import xs_data
import xsection


def load_shares(symbols):
    ciks, out = edgar.ticker_map(ROOT / "data/edgar"), {}
    for s in symbols:
        if s in ciks:
            rec = edgar.company(ciks[s], ROOT / "data/edgar")
            if rec:
                out[s] = (ciks[s], leader_rules.Shares(rec["dei_shares"], rec["gaap_shares"]))
    return out


def timeline(panel, shares, start, lag=1):
    """[(date, leader)] each time the lagged leader changes, from `start`."""
    out, prev = [], None
    for i in range(max(customlib.first_index(panel, start) - lag, 0), len(panel.dates) - lag):
        top = leader_rules.leader(i, panel.dates, panel.adj, panel.raw, shares, panel.members[i])
        if top != prev:
            out.append((str(panel.dates[i + lag]), top))
            prev = top
    return out


def main():
    panel = xs_data.build_panel(date(2015, 1, 1), date(2026, 11, 1))
    shares = load_shares(sorted(panel.adj))
    start = date(2016, 1, 4)
    decide = leader_rules.make_decide(panel, shares)
    r = customlib.run_panel(panel, decide, xsection.Limits(1., 1., 1.), "daily", start)
    i0 = max(customlib.first_index(panel, start) - 1, 0)
    tl = timeline(panel, shares, start)
    held = {}
    for (d, s), (d2, _) in zip(tl, tl[1:] + [(str(panel.dates[-1]), None)]):
        held[s] = held.get(s, 0) + (date.fromisoformat(d2) - date.fromisoformat(d)).days
    ew = [sum(panel.adj[s][i] / panel.adj[s][i0] for s in panel.members[i0] if panel.adj[s][i0] and panel.adj[s][i]) for i in range(i0, len(panel.dates))]
    out = dict(strategy="S&P 500 largest market cap, 100% in one stock, daily check, 1-day lag", result={k: v for k, v in r.items() if k not in ("equity", "dates", "decision_log")},
               switches=len(tl) - 1, calendar_days_as_leader=dict(sorted(held.items(), key=lambda x: -x[1])), timeline=tl,
               benchmarks=dict(SPY_buy_hold_total_return=customlib.buy_hold(panel, "SPY", i0, len(panel.dates) - 1),
                               cash=dict(cagr=0., volatility=0., sharpe=None, max_drawdown=0.)),
               coverage=dict(symbols_in_panel=len(panel.adj), with_edgar_shares=len(shares)))
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("switches", "calendar_days_as_leader", "benchmarks")}, indent=1, default=str)[:1500])
    print(r["metrics"], r["turnover_per_year"], r["costs_pct_of_avg_equity_per_year"])
    for t in tl:
        print(*t)


if __name__ == "__main__":
    main()

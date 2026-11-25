"""5-minute opening-range breakout on a monthly top-20 universe of liquid stocks.

Run from the repo root: python strategies/intraday/orb/run.py. Writes results.json next to this file and the standard
report (REPORT.md, equity.svg, Monte Carlo, trade logs) for each 2 bps run under results/.
"""
import json
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import intraday as I

START, END = date(2020, 1, 1), date(2026, 11, 21)  # END exclusive; Fri 2026-11-20 is the last full session
DAILY_START = date(2016, 1, 1)
SLIPS = (0, 2, 5)
BASE_SLIP = 2
RISK, LEVERAGE, EQUITY = 0.01, 4., 100000.
HERE = Path(__file__).parent


def main():
    started = time.time()
    symbols = list(I.CANDIDATES) + ["SPY"]
    cal = I.calendar(DAILY_START, END)
    daily = I.merge_daily(I.daily_bars(symbols, DAILY_START, END, "raw"), I.daily_bars(symbols, DAILY_START, END, "all"))
    sessions = sorted(d for d in cal if d >= START)
    months = sorted({(d.year, d.month) for d in sessions})
    universe = I.monthly_universe({s: daily[s] for s in I.CANDIDATES if s in daily}, months)
    pairs = sorted({(s, y, m) for (y, m), picked in universe.items() for s in picked})
    fetched = I.prefetch(pairs, END, cal)
    configs = [(short, slip) for short in (True, False) for slip in SLIPS]
    equity = {c: EQUITY for c in configs}
    curves = {c: [] for c in configs}
    trades = {c: [] for c in configs}
    cost = dict.fromkeys(configs, 0.)
    sides = {c: [0, 0] for c in configs}
    logs = {c: [] for c in configs}
    for year, month in months:
        month_days = [d for d in sessions if (d.year, d.month) == (year, month)]
        data = {s: I.month_bars(s, year, month, END, cal) for s in universe[(year, month)]}
        for day in month_days:
            for c in configs:
                short, slip = c
                found = [(s, t) for s, days in data.items()
                         if (bars := days.get(day.isoformat()))
                         and (t := I.orb_day(bars, cal[day][1], slip, short))]
                for symbol, pnl, fee, notional, t in I.settle(I.size_trades(found, equity[c], RISK, LEVERAGE)):
                    equity[c] += pnl
                    cost[c] += fee + notional * slip / 10000 * 2
                    trades[c].append((day, pnl, pnl / notional))
                    sides[c][t["side"] < 0] += 1
                    logs[c].append((day, symbol, t, notional, fee, pnl))
                curves[c].append((day, equity[c]))
    first = sessions[0]
    flat_universe = {s: daily[s] for s in daily}
    picks = lambda d: universe.get((d.year, d.month), [])
    hold = {"SPY": I.buy_hold(flat_universe, lambda d: ["SPY"], sessions),
            "universe_equal_weight": I.buy_hold(flat_universe, picks, sessions)}
    files = [I.DATA / "orb" / f"{s}_{y}-{m:02d}.json" for s, y, m in pairs]
    stored = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    report = dict(
        period=dict(start=str(first), end_exclusive=str(END), last_session=str(sessions[-1]), sessions=len(sessions)),
        rules=dict(risk_per_trade=RISK, leverage_cap=LEVERAGE, start_equity=EQUITY, slippage_bps=SLIPS),
        universe=dict(candidates=len(I.CANDIDATES), per_month=20, distinct_selected=len({s for s, _, _ in pairs}),
                      symbol_months=len(pairs), candidates_without_data=[s for s in I.CANDIDATES if s not in daily]),
        data_volume=dict(symbol_month_files=len(pairs), minute_bars_stored=sum(
            len(bars) for r in stored for bars in r["payload"].values()),
            requests=sum(r["requests"] for r in stored), fetch_seconds_sum=round(sum(r["fetch_seconds"] for r in stored)),
            cache_mb=round(sum(f.stat().st_size for f in files) / 1e6), fetched_this_run=fetched),
        benchmarks={k: dict(metrics=I.metrics(v), yearly=I.yearly(v)) for k, v in hold.items()},
        runs={})
    for (short, slip), curve in curves.items():
        run = I.metrics(curve, trades[(short, slip)], cost[(short, slip)])
        run.update(long_trades=sides[(short, slip)][0], short_trades=sides[(short, slip)][1])
        if slip == BASE_SLIP:
            run["yearly"] = I.yearly(curve)
        report["runs"][f"{'long_short' if short else 'long_only'}_{slip}bps"] = run
    report["wall_seconds"] = round(time.time() - started)
    (HERE / "results.json").write_text(json.dumps(report, indent=1, default=str), encoding="utf-8")
    print("wrote results.json in", report["wall_seconds"], "s")
    for short in (True, False):
        name = f"{'long_short' if short else 'long_only'}_{BASE_SLIP}bps"
        I.write_standard_report(HERE / "results" / name, HERE / f"mc_results_{name}.json", f"intraday-orb {name}",
                                curves[(short, BASE_SLIP)], hold["SPY"], I.orb_fills(logs[(short, BASE_SLIP)]))


if __name__ == "__main__":
    main()

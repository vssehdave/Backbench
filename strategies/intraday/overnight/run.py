"""Overnight (official close to next official open) versus its intraday mirror and buy-and-hold.

Run from the repo root: python strategies/intraday/overnight/run.py. Writes results.json next to this file.
"""
import json
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import alpaca_bars
import intraday as I

START, END = date(2016, 1, 1), date(2026, 11, 21)  # END exclusive; Fri 2026-11-20 is the last full session
EXT_START, EXT_END = date(2016, 1, 1), date(2026, 1, 1)  # range of the cached minute files with extended hours
SLIPS = (0, 2, 5)
BASE_SLIP = 2
HERE = Path(__file__).parent


def summarise(daily, picks, sessions, label):
    """Overnight, intraday mirror and buy-and-hold over `sessions`, for each slippage in SLIPS."""
    out = dict(label=label, first_session=str(sessions[0]), last_session=str(sessions[-1]), runs={})
    hold = I.buy_hold(daily, picks, sessions)
    out["buy_hold"] = I.metrics(hold)
    out["buy_hold_yearly"] = I.yearly(hold)
    for name, build in (("overnight", I.overnight_legs), ("intraday_mirror", I.intraday_legs)):
        legs = build(daily, picks, sessions)
        for slip in SLIPS:
            curve, trades, cost = I.run_legs(legs, sessions, slip)
            run = I.metrics(curve, trades, cost)
            if slip == BASE_SLIP:
                run["yearly"] = I.yearly(curve)
            out["runs"][f"{name}_{slip}bps"] = run
    return out


def extended_legs(symbol, daily, sessions, cal):
    """Buy the last post-close bar's close (16:00-20:00, or to 17:00 on half days), sell the last pre-open bar's close.

    Lower quality: thin extended-hours prints, a bar close stands in for a fill, and no spread is modelled beyond the
    slippage sweep. Prices are scaled by the daily adjusted/raw factor so dividends and splits do not leak in.
    """
    record = alpaca_bars.fetch(symbol, EXT_START, EXT_END)
    after, before, offset = {}, {}, I._offsets()
    for page in record["pages"]["bars"]:
        for r in (page.get("bars") or []):
            t = r["t"]
            moment = alpaca_bars.datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(alpaca_bars.EASTERN)
            day, minute = moment.date(), moment.hour * 60 + moment.minute
            if day not in cal:
                continue
            if 240 <= minute < 570:
                before[day] = (minute, r["c"])  # bars are ascending, so the last one wins
            elif cal[day][1] <= minute < 1200:
                after[day] = (minute, r["c"])
    factor = {d: row[4] / row[1] for d, row in daily[symbol].items()}
    legs, skipped, stale = {}, 0, 0
    for previous, day in zip(sessions, sessions[1:]):
        if previous not in after or day not in before:
            skipped += 1
            continue
        end = 1200 if cal[previous][1] == 960 else 1020
        stale += after[previous][0] < end - 5
        legs[day] = [(symbol, after[previous][1], before[day][1] / after[previous][1] * factor[day] / factor[previous])]
    return legs, dict(skipped_days=skipped, entry_bar_over_5_min_before_session_end=stale)


def main():
    started = time.time()
    symbols = list(I.CANDIDATES) + ["SPY", "QQQ"]
    cal = I.calendar(START, END)
    daily = I.merge_daily(I.daily_bars(symbols, START, END, "raw"), I.daily_bars(symbols, START, END, "all"))
    sessions = sorted(cal)
    assert set(daily["SPY"]) == set(sessions), "SPY daily bars and calendar differ"
    months = sorted({(d.year, d.month) for d in sessions})
    universe = I.monthly_universe({s: daily[s] for s in I.CANDIDATES if s in daily}, months)
    picks = lambda d: universe.get((d.year, d.month), [])
    first = next(d for d in sessions if picks(d))
    report = dict(period=dict(start=str(START), end_exclusive=str(END)), start_equity=100000., slippage_bps=SLIPS,
                  sets={})
    report["sets"]["SPY"] = summarise(daily, lambda d: ["SPY"], sessions, "SPY")
    report["sets"]["QQQ"] = summarise(daily, lambda d: ["QQQ"], sessions, "QQQ")
    report["sets"]["stocks20"] = summarise(daily, picks, [d for d in sessions if d >= first], "top-20 monthly universe")
    report["universe"] = dict(first_month_with_universe=str(first),
                              distinct_symbols=len({s for m in universe.values() for s in m}),
                              candidates_without_data=[s for s in I.CANDIDATES if s not in daily])
    window = [d for d in sessions if d < EXT_END]
    report["extended_hours"] = {}
    for symbol in ("SPY", "QQQ"):
        legs, notes = extended_legs(symbol, daily, window, cal)
        block = dict(notes, window=f"{window[0]}..{window[-1]}",
                     regular_overnight_same_window=summarise(daily, lambda d, s=symbol: [s], window, symbol)["runs"])
        block["runs"] = {}
        for slip in SLIPS:
            curve, trades, cost = I.run_legs(legs, window, slip)
            block["runs"][f"extended_{slip}bps"] = I.metrics(curve, trades, cost)
            if slip == BASE_SLIP:
                block["runs"][f"extended_{slip}bps"]["yearly"] = I.yearly(curve)
        report["extended_hours"][symbol] = block
    report["wall_seconds"] = round(time.time() - started)
    (HERE / "results.json").write_text(json.dumps(report, indent=1, default=str), encoding="utf-8")
    print("wrote results.json in", report["wall_seconds"], "s")


if __name__ == "__main__":
    main()

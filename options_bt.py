"""Monthly-roll covered call (2.2) and protective put (2.4) backtest on one underlying, from daily option bars.

Assumptions, all price-only: option trade closes stand in for quotes, entry pays or receives a fixed half-spread,
expiry settles at intrinsic value against the underlying close (an ITM short call is assigned and the shares are
rebought the same close, which nets to the same cash), no early exercise, no dividends, no interest on cash,
no stock commission. Fees are charged on opening trades only.
"""
import argparse
import json
from datetime import date, timedelta
from pathlib import Path

import options_data as od

MULT = 100
S, H = 0.025, 0.0125  # the paper gives no strikes: one step is 2.5% of spot, a half step 1.25%; nothing is tuned


def leg(kind, qty, offset=0.0, far=False):
    """kind call|put|stock, qty signed (units of n contracts, or n x 100 shares), strike at spot*(1+offset).
    far: expires one monthly cycle later than the rest and is closed at the near expiry."""
    return (kind, qty, offset, far)


def _spread(a, b, kind="call"):  # long strike a, short strike b
    return [leg(kind, +1, a), leg(kind, -1, b)]


def _fly(kind, sign, lo=-S, mid=0.0, hi=S):
    return [leg(kind, sign, lo), leg(kind, -2 * sign, mid), leg(kind, sign, hi)]


def _condor(kind, sign):
    return [leg(kind, sign, -3 * H), leg(kind, -sign, -H), leg(kind, -sign, H), leg(kind, sign, 3 * H)]


def _iron_condor(sign):  # sign +1: long put wing, short put, short call, long call wing
    return [leg("put", sign, -3 * H), leg("put", -sign, -H), leg("call", -sign, H), leg("call", sign, 3 * H)]


def _ladder(kind, sign):  # sign +1: long the near-ATM strike, short two further OTM strikes
    o = 1 if kind == "call" else -1
    return [leg(kind, sign, 0.0), leg(kind, -sign, o * S), leg(kind, -sign, 2 * o * S)]


# name -> (paper section, legs). Existing 2.2 and 2.4 keep their original strikes (2% OTM call, 5% OTM put).
STRATEGIES = {
    "covered_call": ("2.2", [leg("stock", +1), leg("call", -1, 0.02)]),
    "covered_put": ("2.3", [leg("stock", -1), leg("put", -1, -S)]),
    "protective_put": ("2.4", [leg("stock", +1), leg("put", +1, -0.05)]),
    "protective_call": ("2.5", [leg("stock", -1), leg("call", +1, S)]),
    "bull_call_spread": ("2.6", _spread(0.0, S)),
    "bull_put_spread": ("2.7", _spread(-2 * S, -S, "put")),
    "bear_call_spread": ("2.8", _spread(2 * S, S)),
    "bear_put_spread": ("2.9", _spread(0.0, -S, "put")),
    "long_synthetic_forward": ("2.10", [leg("call", +1), leg("put", -1)]),
    "short_synthetic_forward": ("2.11", [leg("put", +1), leg("call", -1)]),
    "long_combo": ("2.12", [leg("call", +1, S), leg("put", -1, -S)]),
    "short_combo": ("2.13", [leg("put", +1, -S), leg("call", -1, S)]),
    "bull_call_ladder": ("2.14", _ladder("call", +1)),
    "bull_put_ladder": ("2.15", _ladder("put", -1)),
    "bear_call_ladder": ("2.16", _ladder("call", -1)),
    "bear_put_ladder": ("2.17", _ladder("put", +1)),
    "calendar_call_spread": ("2.18", [leg("call", +1, 0.0, True), leg("call", -1)]),
    "calendar_put_spread": ("2.19", [leg("put", +1, 0.0, True), leg("put", -1)]),
    "diagonal_call_spread": ("2.20", [leg("call", +1, -0.10, True), leg("call", -1, S)]),
    "diagonal_put_spread": ("2.21", [leg("put", +1, 0.10, True), leg("put", -1, -S)]),
    "long_straddle": ("2.22", [leg("call", +1), leg("put", +1)]),
    "long_strangle": ("2.23", [leg("call", +1, S), leg("put", +1, -S)]),
    "long_guts": ("2.24", [leg("call", +1, -S), leg("put", +1, S)]),
    "short_straddle": ("2.25", [leg("call", -1), leg("put", -1)]),
    "short_strangle": ("2.26", [leg("call", -1, S), leg("put", -1, -S)]),
    "short_guts": ("2.27", [leg("call", -1, -S), leg("put", -1, S)]),
    "long_call_synthetic_straddle": ("2.28", [leg("stock", -1), leg("call", +2)]),
    "long_put_synthetic_straddle": ("2.29", [leg("stock", +1), leg("put", +2)]),
    "short_call_synthetic_straddle": ("2.30", [leg("stock", +1), leg("call", -2)]),
    "short_put_synthetic_straddle": ("2.31", [leg("stock", -1), leg("put", -2)]),
    "covered_short_straddle": ("2.32", [leg("stock", +1), leg("call", -1), leg("put", -1)]),
    "covered_short_strangle": ("2.33", [leg("stock", +1), leg("call", -1, S), leg("put", -1, -S)]),
    "strap": ("2.34", [leg("call", +2), leg("put", +1)]),
    "strip": ("2.35", [leg("call", +1), leg("put", +2)]),
    "call_ratio_backspread": ("2.36", [leg("call", -1), leg("call", +2, S)]),
    "put_ratio_backspread": ("2.37", [leg("put", -1), leg("put", +2, -S)]),
    "ratio_call_spread": ("2.38", [leg("call", +1, -S), leg("call", -2)]),
    "ratio_put_spread": ("2.39", [leg("put", +1, S), leg("put", -2)]),
    "long_call_butterfly": ("2.40", _fly("call", +1)),
    "modified_call_butterfly": ("2.40.1", _fly("call", +1, -2 * S, 0.0, S)),
    "long_put_butterfly": ("2.41", _fly("put", +1)),
    "modified_put_butterfly": ("2.41.1", _fly("put", +1, -2 * S, 0.0, S)),
    "short_call_butterfly": ("2.42", _fly("call", -1)),
    "short_put_butterfly": ("2.43", _fly("put", -1)),
    "long_iron_butterfly": ("2.44", [leg("put", +1, -S), leg("put", -1), leg("call", -1), leg("call", +1, S)]),
    "short_iron_butterfly": ("2.45", [leg("put", -1, -S), leg("put", +1), leg("call", +1), leg("call", -1, S)]),
    "long_call_condor": ("2.46", _condor("call", +1)),
    "long_put_condor": ("2.47", _condor("put", +1)),
    "short_call_condor": ("2.48", _condor("call", -1)),
    "short_put_condor": ("2.49", _condor("put", -1)),
    "long_iron_condor": ("2.50", _iron_condor(+1)),
    "short_iron_condor": ("2.51", _iron_condor(-1)),
    "long_box": ("2.52", [leg("call", +1, -S), leg("call", -1, S), leg("put", +1, S), leg("put", -1, -S)]),
    "collar": ("2.53", [leg("stock", +1), leg("put", +1, -2 * S), leg("call", -1, S)]),
    "bullish_short_seagull": ("2.54", [leg("put", -1, -S), leg("call", +1), leg("call", -1, S)]),
    "bearish_long_seagull": ("2.55", [leg("put", +1, -S), leg("call", -1), leg("call", +1, S)]),
    "bearish_short_seagull": ("2.56", [leg("put", -1, -S), leg("put", +1), leg("call", -1, S)]),
    "bullish_long_seagull": ("2.57", [leg("put", +1, -S), leg("put", -1), leg("call", +1, S)]),
}


def third_friday(year, month):
    first = date(year, month, 1)
    return first + timedelta(days=(4 - first.weekday()) % 7 + 14)


def monthly_expiries(sessions, first, last):
    """Third-Friday expiries in [first, last]; a holiday Friday moves to the previous session."""
    out, year, month = [], first.year, first.month
    while date(year, month, 1) <= last:
        day = third_friday(year, month)
        while day not in sessions and day >= first:
            day -= timedelta(days=1)
        if day in sessions and first <= day <= last:
            out.append(day)
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return out


def max_drawdown(values):
    peak, worst = values[0], 0.0
    for v in values:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1)
    return worst


def run(strategy, closes, expiries, get_contracts, get_closes, capital=100_000.0, half_spread=0.02, fee=0.65):
    """Hold round-lot stock legs bought at the first expiry's close; each cycle open every option leg, n contracts per unit.

    A cycle opens only if every option leg has a bar; otherwise only the stock legs stay (no premium, no fee).
    """
    legs = STRATEGIES[strategy][1]
    options = [l for l in legs if l[0] != "stock"]
    full = expiries
    if any(l[3] for l in options):
        expiries = full[:-1]  # the far leg needs one more expiry after the last cycle
    days = [d for d in sorted(closes) if expiries[0] <= d <= expiries[-1]]
    n = int(capital // (closes[expiries[0]] * MULT))
    bh_shares = n * MULT
    shares = sum(l[1] for l in legs if l[0] == "stock") * bh_shares
    cash0 = capital - shares * closes[expiries[0]]
    cash, equity, cycles = cash0, {}, []
    for i, (e0, e1) in enumerate(zip(expiries, expiries[1:])):
        spot = closes[e0]
        window = [d for d in days if e0 <= d < e1]
        held = []
        for kind, qty, offset, far in options:
            expiry = full[i + 2] if far else e1
            strikes = get_contracts(expiry, kind, spot * 0.8, spot * 1.2)
            strike = min(strikes, key=lambda k: (abs(k - spot * (1 + offset)), k))
            bars = get_closes(strikes[strike], e0, e1)
            first = next((d for d in window if d in bars), None)
            held.append({"kind": kind, "qty": qty, "far": far, "expiry": str(expiry), "symbol": strikes[strike],
                         "strike": strike, "bars": bars, "first": first, "last": None})
        opened = all(h["first"] is not None for h in held)
        cycle = {"entry_date": str(e0), "expiry": str(e1), "opened": opened, "fee": 0.0,
                 "no_bar_days": sum(window.index(h["first"]) for h in held) if opened else len(window),
                 "mark_gap_days": sum(d not in h["bars"] for h in held for d in window if d >= h["first"])
                 if opened else 0}
        if opened:
            for h in held:
                bar = h["bars"][h["first"]]
                fill = max(bar + (1 if h["qty"] > 0 else -1) * half_spread, 0.0)  # long pays up, short receives less
                cash += -h["qty"] * fill * MULT * n - fee * abs(h["qty"]) * n
                cycle["fee"] += fee * abs(h["qty"]) * n
                h.update(bar_close=bar, fill=fill, entry_fill_date=str(h["first"]))
        for d in window:
            value = 0.0
            for h in held:
                h["last"] = h["bars"].get(d, h["last"]) if opened and d >= h["first"] else None
                value += 0 if h["last"] is None else h["qty"] * h["last"] * MULT * n
            equity[d] = cash + shares * closes[d] + value
        final = closes[e1]
        cycle.update(underlying_at_expiry=final, itm=0, assigned=0)
        for h in held:
            long = h["qty"] > 0
            if h["far"]:  # closed at the last known close, paying the half-spread
                if opened:
                    px = h["bars"].get(e1, h["last"])
                    cash += h["qty"] * max(px - (1 if long else -1) * half_spread, 0.0) * MULT * n \
                        - fee * abs(h["qty"]) * n
                    cycle["fee"] += fee * abs(h["qty"]) * n
                    h["closed_at"] = px
            else:
                intrinsic = max(final - h["strike"], 0.0) if h["kind"] == "call" else max(h["strike"] - final, 0.0)
                h["intrinsic"] = intrinsic
                if opened:
                    cash += h["qty"] * intrinsic * MULT * n
                    cycle["itm"] += intrinsic > 0
                    cycle["assigned"] += (not long) and intrinsic > 0  # assigned shares are rebought at the same close
        equity[e1] = cash + shares * final
        cycle["legs"] = [{k: v for k, v in h.items() if k not in ("bars", "last", "first")} for h in held]
        cycles.append(cycle)
    series = [equity[d] for d in days]
    bh = [bh_shares * closes[d] + capital - bh_shares * closes[expiries[0]] for d in days]
    return {
        "strategy": strategy,
        "parameters": {"section": STRATEGIES[strategy][0], "legs": [list(l) for l in legs],
                       "half_spread_per_share": half_spread, "fee_per_contract": fee, "capital": capital,
                       "shares": shares, "contracts_per_unit": n},
        "summary": {"start": str(days[0]), "end": str(days[-1]), "cycles": len(cycles),
                    "cycles_opened": sum(c["opened"] for c in cycles),
                    "no_bar_days": sum(c["no_bar_days"] for c in cycles),
                    "mark_gap_days": sum(c["mark_gap_days"] for c in cycles),
                    "itm_expiries": sum(c["itm"] for c in cycles),
                    "assignments": sum(c["assigned"] for c in cycles),
                    "fees": sum(c["fee"] for c in cycles),
                    "end_equity": series[-1], "total_return": series[-1] / capital - 1,
                    "max_drawdown": max_drawdown(series)},
        "buy_and_hold": {"end_equity": bh[-1], "total_return": bh[-1] / capital - 1,
                         "max_drawdown": max_drawdown(bh)},
        "cycles": cycles,
    }


def describe(strategy):
    parts = []
    for kind, qty, offset, far in STRATEGIES[strategy][1]:
        what = f"{abs(qty) * 100} x n shares" if kind == "stock" else \
            f"{abs(qty)} x n {kind} contracts at spot*{1 + offset:.4f}"
        parts.append(("long " if qty > 0 else "short ") + what +
                     (" (next-next expiry, closed at the near expiry)" if far else ""))
    return "; ".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--underlying", default="SPY")
    parser.add_argument("--start", type=date.fromisoformat, default=date(2024, 1, 19), help="first entry date (a monthly expiry)")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--half-spread", type=float, default=0.02)
    parser.add_argument("--out-dir", default="strategies/catalog", help="catalog folders receive options_results.json")
    args = parser.parse_args()
    # Settled expiries only: the latest third Friday that is not after today.
    closes = od.underlying_closes(args.underlying, args.start, args.today - timedelta(days=1))
    expiries = monthly_expiries(set(closes), args.start, args.today - timedelta(days=1))
    if expiries[0] != args.start:
        raise SystemExit(f"--start {args.start} is not a monthly expiry session; first is {expiries[0]}")
    memo = {}

    def contracts(e, k, lo, hi):
        if (e, k, lo, hi) not in memo:
            memo[e, k, lo, hi] = od.contracts(args.underlying, e, k, lo, hi, args.today)
        return memo[e, k, lo, hi]

    for name, (section, _) in STRATEGIES.items():
        folder = next(Path(args.out_dir).glob(f"{section}-*"))
        results = {"source": "Alpaca historical option bars (trade closes), SPY daily closes",
                   "main": run(name, closes, expiries, contracts, od.option_closes, half_spread=args.half_spread),
                   "half_spread_sensitivity": {str(h): run(name, closes, expiries, contracts, od.option_closes,
                                                          half_spread=h)["summary"]["total_return"]
                                               for h in (0.0, 0.05, 0.10)}}
        (folder / "options_results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        manifest = folder / "options_manifest.json"
        if not manifest.exists():
            m = results["main"]["summary"]
            manifest.write_text(json.dumps({
                "id": f"cat-{folder.name}-options", "version": "1", "runner": "options_bt.py", "strategy": name,
                "data": {"kind": "alpaca_options", "underlying": args.underlying, "bars": "1Day option trade closes",
                         "history_from": "2024-01-18"},
                "rule": f"Each month from one monthly expiry to the next, held to expiry: {describe(name)}.",
                "strike_rule": "nearest listed strike to spot*(1+offset), spot = underlying close on the roll date; "
                               "offsets are fixed (step 2.5% of spot, half step 1.25%), not tuned",
                "capital": 100000.0,
                "half_spread_per_share": {"value": args.half_spread, "status": "ASSUMPTION: bars are trade prices, "
                                          "no historical quotes exist; entry pays/receives this per share"},
                "fee_per_contract": 0.65,
                "settlement": "intrinsic value vs underlying close at expiry; far legs closed at the last bar at the near expiry",
                "benchmark": "buy_and_hold SPY, same lots, same dates", "start": m["start"], "end": m["end"]},
                indent=2) + "\n", encoding="utf-8")
        s, b = results["main"]["summary"], results["main"]["buy_and_hold"]
        print(f"{section} {name}: {s['total_return']:.1%} (maxDD {s['max_drawdown']:.1%}) vs B&H {b['total_return']:.1%} "
              f"(maxDD {b['max_drawdown']:.1%}); opened {s['cycles_opened']}/{s['cycles']}, "
              f"no_bar_days {s['no_bar_days']}, mark_gap_days {s['mark_gap_days']}, assigned {s['assignments']}")


if __name__ == "__main__":
    main()

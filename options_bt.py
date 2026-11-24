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
# kind, side (+1 long the option, -1 short it), distance of the strike from spot (OTM fraction)
STRATEGIES = {"covered_call": ("call", -1, 0.02), "protective_put": ("put", +1, 0.05)}


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


def run(strategy, closes, expiries, get_contracts, get_closes, capital=100_000.0, half_spread=0.02, fee=0.65,
        otm=None):
    """Hold round-lot shares bought at the first expiry's close; each cycle open one option per 100 shares."""
    kind, side, default_otm = STRATEGIES[strategy]
    otm = default_otm if otm is None else otm
    days = [d for d in sorted(closes) if expiries[0] <= d <= expiries[-1]]
    shares = int(capital // (closes[expiries[0]] * MULT)) * MULT
    cash0 = capital - shares * closes[expiries[0]]
    n = shares // MULT
    cash, equity, cycles = cash0, {}, []
    for e0, e1 in zip(expiries, expiries[1:]):
        spot = closes[e0]
        strikes = get_contracts(e1, kind, spot * 0.8, spot * 1.2)
        target = spot * (1 + otm if kind == "call" else 1 - otm)
        strike = min(strikes, key=lambda k: (abs(k - target), k))
        bars = get_closes(strikes[strike], e0, e1)
        window = [d for d in days if e0 <= d < e1]
        first = next((d for d in window if d in bars), None)
        cycle = {"entry_date": str(e0), "expiry": str(e1), "symbol": strikes[strike], "strike": strike,
                 "no_bar_days": len(window) if first is None else window.index(first),
                 "mark_gap_days": 0 if first is None else sum(d not in bars for d in window if d >= first)}
        if first is not None:
            fill = max(bars[first] + side * half_spread, 0.0)  # long pays up, short receives less
            cash += -side * fill * MULT * n - fee * n
            cycle.update(entry_fill_date=str(first), bar_close=bars[first], fill=fill, fee=fee * n)
        last = None
        for d in window:
            last = bars.get(d, last) if first is not None and d >= first else None
            equity[d] = cash + shares * closes[d] + (0 if last is None else side * last * MULT * n)
        final = closes[e1]
        intrinsic = max(final - strike, 0.0) if kind == "call" else max(strike - final, 0.0)
        cycle.update(underlying_at_expiry=final, intrinsic=intrinsic, opened=first is not None,
                     itm=intrinsic > 0, assigned=side < 0 and first is not None and intrinsic > 0)
        if first is not None:
            cash += side * intrinsic * MULT * n
        equity[e1] = cash + shares * final
        cycles.append(cycle)
    series = [equity[d] for d in days]
    held = [shares * closes[d] + cash0 for d in days]
    return {
        "strategy": strategy,
        "parameters": {"kind": kind, "side": "short" if side < 0 else "long", "otm_fraction": otm,
                       "half_spread_per_share": half_spread, "fee_per_contract": fee, "capital": capital,
                       "shares": shares, "contracts": n},
        "summary": {"start": str(days[0]), "end": str(days[-1]), "cycles": len(cycles),
                    "cycles_opened": sum(c["opened"] for c in cycles),
                    "no_bar_days": sum(c["no_bar_days"] for c in cycles),
                    "mark_gap_days": sum(c["mark_gap_days"] for c in cycles),
                    "itm_expiries": sum(c["itm"] for c in cycles if c["opened"]),
                    "assignments": sum(c["assigned"] for c in cycles),
                    "fees": sum(c.get("fee", 0.0) for c in cycles),
                    "end_equity": series[-1], "total_return": series[-1] / capital - 1,
                    "max_drawdown": max_drawdown(series)},
        "buy_and_hold": {"end_equity": held[-1], "total_return": held[-1] / capital - 1,
                         "max_drawdown": max_drawdown(held)},
        "cycles": cycles,
    }


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
    contracts = lambda e, k, lo, hi: od.contracts(args.underlying, e, k, lo, hi, args.today)
    folders = {"covered_call": "2.2-covered-call", "protective_put": "2.4-protective-put"}
    for name, folder in folders.items():
        results = {"source": "Alpaca historical option bars (trade closes), SPY daily closes",
                   "main": run(name, closes, expiries, contracts, od.option_closes, half_spread=args.half_spread),
                   "half_spread_sensitivity": {str(h): run(name, closes, expiries, contracts, od.option_closes,
                                                          half_spread=h)["summary"]["total_return"]
                                               for h in (0.0, 0.05, 0.10)}}
        path = Path(args.out_dir) / folder / "options_results.json"
        path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        s, b = results["main"]["summary"], results["main"]["buy_and_hold"]
        print(f"{name}: {s['total_return']:.1%} (maxDD {s['max_drawdown']:.1%}) vs B&H {b['total_return']:.1%} "
              f"(maxDD {b['max_drawdown']:.1%}); opened {s['cycles_opened']}/{s['cycles']}, "
              f"no_bar_days {s['no_bar_days']}, mark_gap_days {s['mark_gap_days']}, assigned {s['assignments']}")


if __name__ == "__main__":
    main()

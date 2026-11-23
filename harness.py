"""Single-symbol USD equity research replay. Run with python harness.py --help."""
import argparse
import hashlib
import importlib
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path


def fixture():
    day = date(2022, 1, 1)
    rows = []
    while day < date(2024, 1, 1):
        if day.weekday() < 5:
            i = len(rows)
            rows.append((day, 100 + 5 * math.sin(i / 12), 100 + 5 * math.sin((i + 0.5) / 12)))
        day += timedelta(days=1)
    return rows


def qlib_rows(provider, symbol, start, end):
    import qlib
    from qlib.data import D

    qlib.init(provider_uri=str(Path(provider).resolve()), region="us")
    bars = D.features([symbol], ["$open", "$close"], start_time=start, end_time=end, freq="day")
    return [(ts.date(), float(o), float(c)) for (_, ts), (o, c) in bars.sort_index().iterrows()]


def fees(delta, price):
    """Current IBKR Pro US fixed base + separately estimated regulatory fees, USD."""
    qty = abs(delta)
    value = qty * price
    commission = min(max(1, qty * 0.005), value * 0.01) if qty else 0
    regulatory = qty * 0.000003 + (value * 0.0000206 if delta < 0 else 0)
    return commission, regulatory


def months_after(start, months):
    month = start.month + months
    return date(start.year + (month > 12), (month - 1) % 12 + 1, 1)


def replay(rows, strategy, level, state, history, seed=None, shock_bps=0):
    cash, shares = state
    history = list(history)
    rng = random.Random(seed)
    multiplier = 1.0
    fills, equity = [], []
    for day, opening, closing in rows:
        # A return innovation scales both today's open and close and propagates forward.
        multiplier *= math.exp(rng.gauss(0, shock_bps / 10000)) if shock_bps else 1
        opening *= multiplier
        closing *= multiplier
        target = strategy(tuple(history), level) if history else shares
        if type(target) is not int or target < 0:
            raise ValueError("Expected nonnegative integer target position")
        delta = target - shares
        commission, regulatory = fees(delta, opening)
        debit = delta * opening + commission + regulatory
        if delta and cash >= debit:
            cash -= debit
            shares = target
            fills.append(dict(date=str(day), shares=delta, price=opening,
                              commission=commission, regulatory=regulatory))
        history.append(closing)
        equity.append(cash + shares * closing)
    return (cash, shares), equity, fills


def trend_attribution(train, forward, equity, starting_equity):
    """Attribute each close-to-close change to the trend known at that open."""
    history = [r[2] for r in train]
    groups = {}
    previous = starting_equity
    for row, marked in zip(forward, equity, strict=True):
        regime = "insufficient_history"
        if len(history) >= 21:
            change = history[-1] - history[-21]
            regime = "rising" if change > 0 else "falling" if change < 0 else "flat"
        group = groups.setdefault(regime, {"sessions": 0, "net_pnl_usd": 0.})
        group["sessions"] += 1
        group["net_pnl_usd"] += marked - previous
        previous = marked
        history.append(row[2])
    return groups


def study(rows, strategy, levels, paths, shock_bps, seed, start, end):
    if not rows or any(not all(math.isfinite(x) and x > 0 for x in r[1:]) for r in rows):
        raise ValueError("Expected positive finite OHLC observations")
    dates = [r[0] for r in rows]
    if dates != sorted(set(dates)):
        raise ValueError("Expected unique, ordered daily observations")
    results = []
    while months_after(start, 12) <= end:
        split = months_after(start, 6)
        stop = months_after(split, 6)
        train = [r for r in rows if start <= r[0] < split]
        forward = [r for r in rows if split <= r[0] < stop]
        if not train or not forward:
            raise ValueError("Empty training or forward window")
        fit = getattr(strategy, "fit", None)
        decide = strategy.decide if fit else strategy
        selection_rows = train
        warmup = []
        prefix = []
        if fit:
            inner_cut = months_after(start, 3)
            prefix = [r for r in train if r[0] < inner_cut]
            selection_rows = [r for r in train if r[0] >= inner_cut]
            if not prefix or not selection_rows:
                raise ValueError("Fitted strategies require observations in both training halves")
            warmup = [r[2] for r in prefix]
        scores = {}
        for p in levels:
            parameter = fit(tuple(prefix), p) if fit else p
            scores[p] = replay(selection_rows, decide, parameter, (10000., 0), warmup)[1][-1]
        best = max(levels, key=scores.get)
        # Fit using only this batch. Each artifact must be immutable and decisions pure.
        artifacts = {p: fit(tuple(train), p) if fit else p for p in levels}
        history = [r[2] for r in train]
        opening_state = (10000., 0)
        _, equity, fills = replay(forward, decide, artifacts[best], opening_state, history)
        selection_return = scores[best] / opening_state[0] - 1
        train_return = None if fit else selection_return
        forward_return = equity[-1] / opening_state[0] - 1
        neighbours = {p: replay(forward, decide, artifacts[p], opening_state, history)[1][-1] for p in levels}
        scenarios = []
        for i in range(paths):
            path_seed = seed + len(results) * paths + i
            _, curve, trades = replay(forward, decide, artifacts[best], opening_state, history,
                                      path_seed, shock_bps)
            scenarios.append(dict(seed=path_seed, ending_equity=curve[-1], fills=len(trades)))
        results.append(dict(train_start=str(start), forward_start=str(split), end_exclusive=str(stop),
                            selected=best, train_scores=scores, sensitivity=neighbours,
                            train_return=train_return, forward_return=forward_return,
                            selection_start=str(selection_rows[0][0]), selection_return=selection_return,
                            forward_minus_train=None if fit else forward_return - train_return,
                            forward_buys=sum(t["shares"] > 0 for t in fills),
                            forward_sells=sum(t["shares"] < 0 for t in fills),
                            trend_regimes=trend_attribution(train, forward, equity, opening_state[0]),
                            equity=equity, fills=fills, scenarios=scenarios))
        start = stop
    if not results:
        raise ValueError("Supply at least twelve complete calendar months")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", default="controls:threshold")
    parser.add_argument("--levels", nargs="+", type=float, default=[98., 100., 102.])
    parser.add_argument("--paths", type=int, default=20)
    parser.add_argument("--shock-bps", type=float, default=10.)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--provider", help="Local Qlib provider with as-traded USD whole-share prices")
    parser.add_argument("--symbol", default="FIXTURE")
    parser.add_argument("--start", type=date.fromisoformat, default=date(2022, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date(2024, 1, 1), help="Exclusive")
    parser.add_argument("--out", type=Path, default=Path("run.json"))
    args = parser.parse_args()
    if (args.start.day != 1 or args.paths < 1 or not math.isfinite(args.shock_bps)
            or args.shock_bps < 0 or not all(map(math.isfinite, args.levels))):
        parser.error("Use a month-start date, positive path count and finite parameters")
    module, name = args.strategy.split(":")
    strategy = getattr(importlib.import_module(module), name)
    rows = qlib_rows(args.provider, args.symbol, args.start.isoformat(),
                     (args.end - timedelta(days=1)).isoformat()) if args.provider else fixture()
    if not rows or rows[0][0] > args.start + timedelta(days=7) or rows[-1][0] < args.end - timedelta(days=8):
        parser.error("Data does not cover the requested research period")
    report = dict(config=vars(args), data_sha256=hashlib.sha256(repr(rows).encode()).hexdigest(),
                  currency="USD", source="qlib" if args.provider else "synthetic",
                  folds=study(rows, strategy, args.levels, args.paths, args.shock_bps,
                              args.seed, args.start, args.end))
    args.out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()

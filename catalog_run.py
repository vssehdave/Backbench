"""Multi-symbol OHLCV walk-forward for catalog rules. Run with python catalog_run.py --help.

Same folds (6 months train, 6 months forward, 12-month steps), fee model, next-open fills, borrow accrual and margin
guard as harness.py; rules see full OHLCV history of every symbol (including data before the first train window).
A rule is decide(hist, level) -> None (hold) | weights {symbol: float}. Weight 1.0 is a 5,000 USD unit (half of the
10,000 USD start cash, as in the single-instrument catalog runs). Shares are fixed between changes of the weights;
return Rebalance(weights) to re-size at the open even when the weights are unchanged.
"""
import argparse
import hashlib
import importlib
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

import catalog_data
import harness
from spot import Spot

START_CASH, UNIT, MAX_GROSS = 10000., 5000., 2.


class Rebalance(dict):
    """Weights that are re-applied to share counts even if equal to the previous weights."""


def align(series):
    """{symbol: rows (day, o, h, l, c, v)} -> {symbol: rows} on the dates every symbol has."""
    common = set.intersection(*(set(r[0] for r in rows) for rows in series.values()))
    return {s: [r for r in rows if r[0] in common] for s, rows in series.items()}


def replay(bars, decide, level, state, hist, warmup=0, short=None, spot=None, log=None):
    """bars: {symbol: aligned rows to trade}; hist: {symbol: rows before bars}; state: (cash, {symbol: lots})."""
    symbols = list(bars)
    cash, lots = state[0], dict(state[1])
    for s in symbols:
        lots.setdefault(s, 0)
    hist = {s: list(hist[s]) for s in symbols}
    lot = spot.lot_size if spot else 1
    last, wiped, previous = None, False, None
    fills, equity = [], []
    for i in range(len(bars[symbols[0]])):
        day = bars[symbols[0]][i][0]
        opens = {s: bars[s][i][1] for s in symbols}
        closes = {s: bars[s][i][4] for s in symbols}
        if short is not None and previous:
            for s in symbols:
                if lots[s] < 0:
                    cash -= -lots[s] * lot * previous[1][s] * short / 10000 * (day - previous[0]).days / 365
        previous = day, closes
        weights = decide(hist, level) if len(hist[symbols[0]]) >= max(warmup, 1) else None
        if weights is None and log is not None:
            log["abstentions"] += 1
        if weights is not None:
            if not set(weights) <= set(symbols) or not all(math.isfinite(w) for w in weights.values()):
                raise ValueError(f"Bad weights {weights}")
            if sum(abs(w) for w in weights.values()) > MAX_GROSS + 1e-9 or (short is None and min(weights.values(), default=0) < 0):
                raise ValueError(f"Weights exceed gross {MAX_GROSS} or short without allow_short: {weights}")
            if isinstance(weights, Rebalance) or weights != last:
                last = dict(weights)
                # Size from the last close, sells before buys so proceeds fund the buys.
                target = {s: int(weights.get(s, 0) * UNIT / (lot * hist[s][-1][4])) for s in symbols}
                for s in sorted(symbols, key=lambda s: target[s] - lots[s]):
                    delta = target[s] - lots[s]
                    if not delta:
                        continue
                    value = delta * lot * opens[s]
                    commission, regulatory = (spot.commission(value), 0.) if spot else harness.fees(delta, opens[s])
                    debit = value + commission + regulatory
                    if spot and abs(value) < spot.min_notional_usd or cash < debit or wiped:
                        if log is not None:
                            log["rejected"] = log.get("rejected", 0) + 1
                        continue
                    cash -= debit
                    lots[s] = target[s]
                    fills.append(dict(date=str(day), symbol=s, lots=delta, price=opens[s], commission=commission,
                                      regulatory=regulatory))
        for s in symbols:
            hist[s].append(bars[s][i])
        marked = cash + sum(lots[s] * lot * closes[s] for s in symbols)
        if short is not None and any(v < 0 for v in lots.values()) and marked <= 0:
            for s in symbols:
                if lots[s]:
                    commission, regulatory = (spot.commission(lots[s] * lot * closes[s]), 0.) if spot \
                        else harness.fees(-lots[s], closes[s])
                    cash += lots[s] * lot * closes[s] - commission - regulatory
                    fills.append(dict(date=str(day), symbol=s, lots=-lots[s], price=closes[s], commission=commission,
                                      regulatory=regulatory, forced=True))
                    lots[s] = 0
            wiped, marked = True, cash
            if log is not None:
                log["forced_closes"] = log.get("forced_closes", 0) + 1
        equity.append(marked)
    return (cash, lots), equity, fills


def hold(weights):
    return lambda hist, level: weights


def study(rows, decide, levels, bench_weights, start, end, warmup=0, short=None, spot=None):
    rows = align(rows)
    first = next(iter(rows))
    days = [r[0] for r in rows[first]]
    folds = []
    while harness.months_after(start, 12) <= end:
        split = harness.months_after(start, 6)
        stop = harness.months_after(split, 6)

        def cut(lo, hi):
            return {s: [r for r in v if lo <= r[0] < hi] for s, v in rows.items()}, {s: [r for r in v if r[0] < lo] for s, v in rows.items()}

        train, before_train = cut(start, split)
        forward, before_forward = cut(split, stop)
        if not train[first] or not forward[first]:
            raise ValueError("Empty training or forward window")
        scores = {p: replay(train, decide, p, (START_CASH, {}), before_train, warmup, short, spot)[1][-1] for p in levels}
        best = max(levels, key=scores.get)
        log = {"abstentions": 0, "forced_closes": 0}
        _, equity, fills = replay(forward, decide, best, (START_CASH, {}), before_forward, warmup, short, spot, log)
        sensitivity = {p: replay(forward, decide, p, (START_CASH, {}), before_forward, warmup, short, spot)[1][-1] / START_CASH - 1
                       for p in levels}
        bench = replay(forward, hold(bench_weights), None, (START_CASH, {}), before_forward, 0, None, spot)[1][-1]
        folds.append(dict(forward_start=str(split), end_exclusive=str(stop), selected=best,
                          train_scores={p: v / START_CASH - 1 for p, v in scores.items()}, sensitivity=sensitivity,
                          forward_return=equity[-1] / START_CASH - 1, benchmark_return=bench / START_CASH - 1,
                          abstentions=log["abstentions"], forced_closes=log["forced_closes"],
                          rejected=log.get("rejected", 0), buys=sum(f["lots"] > 0 for f in fills),
                          sells=sum(f["lots"] < 0 for f in fills), max_drawdown=harness.max_drawdown(equity, START_CASH),
                          equity=equity, fills=fills))
        start = stop
    if not folds:
        raise ValueError("Supply at least twelve complete calendar months")
    return folds


def compound(values):
    total = 1.
    for v in values:
        total *= 1 + v
    return total - 1


REQUIRED = {"id", "entry", "data", "levels", "warmup", "benchmark", "costs"}


def load_manifest(path):
    m = json.loads(Path(path).read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - m.keys())
    if missing:
        raise ValueError(f"{path}: missing {missing}")
    if not m["levels"] or not set(m["benchmark"]) <= set(m["data"]["symbols"]):
        raise ValueError(f"{path}: levels must be non-empty and benchmark symbols must be in data.symbols")
    if "borrow_bps_per_year" in m and not m.get("allow_short"):
        raise ValueError(f"{path}: borrow_bps_per_year needs allow_short")
    return m


def load_rows(manifest, start):
    data = manifest["data"]
    if data["kind"] == "kraken":
        return {s: catalog_data.kraken_daily(s) for s in data["symbols"]}
    lo = str(date(start.year - 2, 1, 1))
    return {s: catalog_data.alpaca_daily(s, lo, data.get("to", "2026-01-01")) for s in data["symbols"]}


def run(manifest_path, start, end):
    manifest = load_manifest(manifest_path)
    sys.path.insert(0, str(Path(manifest_path).resolve().parent))
    decide = importlib.import_module(manifest["entry"].split(":")[0])
    decide = getattr(decide, manifest["entry"].split(":")[1])
    costs = manifest["costs"]
    spot = Spot(costs["fee_bps"], costs["lot"], costs["min_usd"]) if isinstance(costs, dict) else None
    short = manifest.get("borrow_bps_per_year", 0) if manifest.get("allow_short") else None
    rows = load_rows(manifest, start)
    first = min(r[0][0] for r in rows.values()), max(r[0][0] for r in rows.values())
    if first[1] > start + timedelta(days=7) or max(r[-1][0] for r in rows.values()) < end - timedelta(days=8):
        raise ValueError(f"Data does not cover {start}..{end}; latest first bar {first[1]}")
    folds = study(rows, decide, manifest["levels"], manifest["benchmark"], start, end, manifest["warmup"], short, spot)
    return dict(manifest=manifest, config=dict(start=str(start), end=str(end)),
                data_sha256=hashlib.sha256(repr(rows).encode()).hexdigest(),
                execution_contract=dict(engine_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                        fee_profile=spot.profile if spot else harness.FEE_PROFILE,
                                        starting_cash=START_CASH, unit_usd=UNIT, price_adjustment="split+dividend (all)"),
                summary=dict(strategy=compound(f["forward_return"] for f in folds),
                             benchmark=compound(f["benchmark_return"] for f in folds), cash=0.,
                             beats_benchmark=sum(f["forward_return"] > f["benchmark_return"] for f in folds),
                             folds=len(folds)),
                folds=folds)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("manifest", type=Path)
    p.add_argument("--start", type=date.fromisoformat, default=date(2016, 1, 1))
    p.add_argument("--end", type=date.fromisoformat, default=date(2026, 1, 1), help="Exclusive")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        result = run(args.manifest, args.start, args.end)
    except (OSError, ValueError, KeyError) as exc:
        p.exit(2, f"failed: {exc}\n")
    args.out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    for f in result["folds"]:
        print(f"{f['forward_start']}..{f['end_exclusive']} sel={f['selected']} strat={f['forward_return']:.2%} "
              f"bench={f['benchmark_return']:.2%} fills={f['buys']}+{f['sells']} forced={f['forced_closes']}")
    s = result["summary"]
    print(f"compounded strategy={s['strategy']:.2%} benchmark={s['benchmark']:.2%} beats={s['beats_benchmark']}/{s['folds']}")


if __name__ == "__main__":
    main()

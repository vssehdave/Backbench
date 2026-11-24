"""Single-symbol USD equity research replay. Run with python harness.py --help."""
import argparse
import hashlib
import importlib
import json
import math
import random
from collections import deque
from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path
from stress import StressConfig, max_drawdown
from spot import Spot, spot_fixture


def engine_digest(root=None):
    """Identify the core replay and stress implementation across checkouts."""
    root = Path(__file__).resolve().parent if root is None else Path(root)
    sources = {}
    for name in ("harness.py", "stress.py"):
        # Universal newlines keep a Windows checkout comparable with a POSIX checkout.
        source = (root / name).read_text(encoding="utf-8")
        sources[name] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    manifest = json.dumps(sources, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest()


FEE_PROFILE = "ibkr-us-fixed-2026-11-22"


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


def replay(rows, strategy, level, state, history, seed=None, shock_bps=0, stress=None, spot=None, log=None,
           short=None):
    """short is None (long-only) or the annual borrow rate in bps; it also allows negative targets."""
    cash, shares = state
    history = list(history)
    rng = random.Random(seed)
    multiplier = 1.0
    targets = deque()
    execution_rng = random.Random(f"{seed}:execution")
    fills, equity = [], []
    previous, wiped = None, False
    for day, opening, closing in rows:
        # A return innovation scales both today's open and close and propagates forward.
        multiplier *= math.exp(rng.gauss(0, shock_bps / 10000)) if shock_bps else 1
        opening *= multiplier
        closing *= multiplier
        if short is not None and shares < 0 and previous:
            # Borrow accrues on the short value held since the last close, over calendar days (as in xsection).
            cash -= -shares * previous[1] * short / 10000 * (day - previous[0]).days / 365
        previous = day, closing
        target = strategy(tuple(history), level) if history else shares
        if target is None and log is not None:
            log["abstentions"] += 1
        if target is not None and (type(target) is not int or (target < 0 and short is None)):
            raise ValueError("Expected nonnegative integer target position (negative needs allow_short), or None to hold")
        if stress:
            # An abstention is queued as None so a delayed hold never reverts to a stale position.
            targets.append(target)
            target = targets.popleft() if len(targets) > stress.delay_sessions else None
        if target is None:
            target = shares
        delta = target - shares
        if stress:
            # One draw per session makes rejections comparable across strategies.
            if execution_rng.random() < stress.reject_probability:
                delta = 0
            elif delta:
                opening *= 1 + math.copysign(stress.half_spread_bps / 10000, delta)
        quantity = delta * spot.lot_size if spot else delta
        order_value = quantity * opening
        commission, regulatory = (spot.commission(order_value), 0.) if spot else fees(delta, opening)
        debit = order_value + commission + regulatory
        meets_minimum = not spot or abs(order_value) >= spot.min_notional_usd
        if delta and meets_minimum and cash >= debit and not wiped:
            cash -= debit
            shares = target
            fills.append(dict(date=str(day), shares=quantity, lots=delta, quantity=quantity, price=opening,
                              commission=commission, regulatory=regulatory))
        history.append(closing)
        held_quantity = shares * spot.lot_size if spot else shares
        if short is not None and shares and cash + held_quantity * closing <= 0:
            # Margin call: flatten at the close and stop trading this replay.
            commission, regulatory = fees(-shares, closing)
            cash -= -shares * closing + commission + regulatory
            fills.append(dict(date=str(day), shares=-shares, lots=-shares, quantity=-shares, price=closing,
                              commission=commission, regulatory=regulatory, forced=True))
            shares, held_quantity, wiped = 0, 0, True
            if log is not None:
                log["forced_closes"] = log.get("forced_closes", 0) + 1
        equity.append(cash + held_quantity * closing)
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


def study(rows, strategy, levels, paths, shock_bps, seed, start, end, stress_config=StressConfig(), spot=None, short=None):
    if not rows or any(not all(math.isfinite(x) and x > 0 for x in r[1:]) for r in rows):
        raise ValueError("Expected positive finite OHLC observations")
    dates = [r[0] for r in rows]
    if dates != sorted(set(dates)):
        raise ValueError("Expected unique, ordered daily observations")
    if spot:
        expected = (end - start).days
        if sum(start <= day < end for day in dates) != expected:
            raise ValueError("Spot replay requires a bar for every UTC date in the requested interval")
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
            scores[p] = replay(selection_rows, decide, parameter, (10000., 0), warmup, spot=spot, short=short)[1][-1]
        best = max(levels, key=scores.get)
        # Fit using only this batch. Each artifact must be immutable and decisions pure.
        artifacts = {p: fit(tuple(train), p) if fit else p for p in levels}
        history = [r[2] for r in train]
        opening_state = (10000., 0)
        log = {"abstentions": 0, "forced_closes": 0}
        _, equity, fills = replay(forward, decide, artifacts[best], opening_state, history, spot=spot, log=log,
                                  short=short)
        selection_return = scores[best] / opening_state[0] - 1
        train_return = None if fit else selection_return
        forward_return = equity[-1] / opening_state[0] - 1
        neighbours = {p: replay(forward, decide, artifacts[p], opening_state, history, spot=spot, short=short)[1][-1] for p in levels}
        scenarios = []
        original = {(t["date"], t["shares"]) for t in fills}
        for i in range(paths):
            path_seed = seed + len(results) * paths + i
            draw = stress_config.draw(path_seed, levels, best)
            _, curve, trades = replay(forward, decide, artifacts[draw.level], opening_state, history,
                                      path_seed, shock_bps, draw, spot, short=short)
            simulated = {(t["date"], t["shares"]) for t in trades}
            scenarios.append(dict(seed=path_seed, ending_equity=curve[-1], fills=len(trades),
                                  perturbations=asdict(draw), drawdown=max_drawdown(curve, opening_state[0]),
                                  ending_delta_usd=curve[-1]-equity[-1], added_fills=len(simulated-original),
                                  removed_fills=len(original-simulated)))
        results.append(dict(train_start=str(start), forward_start=str(split), end_exclusive=str(stop),
                            selected=best, train_scores=scores, sensitivity=neighbours,
                            train_return=train_return, forward_return=forward_return,
                            selection_start=str(selection_rows[0][0]), selection_return=selection_return,
                            forward_minus_train=None if fit else forward_return - train_return,
                            abstentions=log["abstentions"], forced_closes=log["forced_closes"],
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
    parser.add_argument("--max-delay-sessions", type=int, default=0)
    parser.add_argument("--max-half-spread-bps", type=float, default=0.)
    parser.add_argument("--reject-probability", type=float, default=0.)
    parser.add_argument("--neighbour-steps", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--spot-fixture", action="store_true", help="Synthetic 24/7 USD spot-market bars")
    sources.add_argument("--provider", help="Local Qlib provider with as-traded USD whole-share prices")
    sources.add_argument("--minute-csv", type=Path, help="Local VWAP TT minute OHLCV file")
    sources.add_argument("--alpaca", action="store_true", help="Alpaca SIP one-minute bars, raw prices")
    parser.add_argument("--allow-splits", action="store_true", help="Accept splits inside an --alpaca range")
    parser.add_argument("--alpaca-dir", type=Path, default=Path("data/alpaca"), help="Raw Alpaca cache")
    parser.add_argument("--symbol", default="FIXTURE")
    parser.add_argument("--spot-fee-bps", type=float, help="Assumed spot fee per side, charged in USD")
    parser.add_argument("--spot-lot", type=float, help="Base asset units per lot")
    parser.add_argument("--spot-min-usd", type=float, help="Minimum eligible order value in USD")
    parser.add_argument("--start", type=date.fromisoformat, default=date(2022, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date(2024, 1, 1), help="Exclusive")
    parser.add_argument("--out", type=Path, default=Path("run.json"))
    args = parser.parse_args()
    spot = None
    assumptions = [args.spot_fee_bps, args.spot_lot, args.spot_min_usd]
    if args.spot_fixture:
        if None in assumptions:
            parser.error("--spot-fixture requires --spot-fee-bps, --spot-lot and --spot-min-usd")
        try:
            spot = Spot(*assumptions)
        except ValueError as exc:
            parser.error(str(exc))
    elif any(value is not None for value in assumptions):
        parser.error("Spot costs and lots require --spot-fixture")
    try:
        stress_config = StressConfig(args.max_delay_sessions, args.max_half_spread_bps,
                                     args.reject_probability, args.neighbour_steps)
    except ValueError as exc:
        parser.error(str(exc))
    if (args.start.day != 1 or args.paths < 1 or not math.isfinite(args.shock_bps)
            or args.shock_bps < 0 or not all(map(math.isfinite, args.levels))):
        parser.error("Use a month-start date, positive path count and finite parameters")
    module, name = args.strategy.split(":")
    strategy = getattr(importlib.import_module(module), name)
    quality = {}
    if args.spot_fixture:
        rows, source = spot_fixture(), "synthetic_spot_utc"
    elif args.minute_csv:
        from minute_bars import daily_from_minutes
        if args.symbol == "FIXTURE":
            parser.error("--minute-csv requires --symbol")
        rows, quality = daily_from_minutes(args.minute_csv, args.symbol, args.start, args.end)
        source = "minute_csv"
    elif args.alpaca:
        from alpaca_bars import daily_from_alpaca
        if args.symbol == "FIXTURE":
            parser.error("--alpaca requires --symbol")
        try:
            rows, quality = daily_from_alpaca(args.symbol, args.start, args.end, "sip", args.alpaca_dir,
                                              args.allow_splits)
        except (ValueError, RuntimeError) as exc:
            parser.error(str(exc))
        source = "alpaca_sip_raw"
    elif args.provider:
        rows = qlib_rows(args.provider, args.symbol, args.start.isoformat(),
                         (args.end - timedelta(days=1)).isoformat())
        source = "qlib"
    else:
        rows, source = fixture(), "synthetic"
    if not rows or rows[0][0] > args.start + timedelta(days=7) or rows[-1][0] < args.end - timedelta(days=8):
        parser.error("Data does not cover the requested research period")
    # Paths are machine-specific. Source and the content digest identify the actual input.
    config = {key: value for key, value in vars(args).items()
              if key not in {"provider", "minute_csv", "alpaca_dir", "out"}}
    report = dict(config=config, data_sha256=hashlib.sha256(repr(rows).encode()).hexdigest(),
                  execution_contract=dict(engine_sha256=engine_digest(),
                                          fee_profile=spot.profile if spot else FEE_PROFILE,
                                          starting_cash=10000.0),
                  currency="USD", source=source, data_quality=quality,
                  folds=study(rows, strategy, args.levels, args.paths, args.shock_bps,
                              args.seed, args.start, args.end, stress_config, spot))
    args.out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()

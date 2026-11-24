"""Intraday research on Alpaca SIP bars: overnight (close to open) legs and 5-minute opening-range breakouts.

Official opens and closes come from SIP 1Day bars, never from minute bars (the closing auction is missing from
the last minute). Fees are harness.fees (IBKR-style). See docs/intraday.md.
"""
import hashlib
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import alpaca_bars
import harness

DATA = Path("data/intraday")
OPEN_MIN, REGULAR_CLOSE, EXIT_BEFORE_CLOSE = 570, 960, 5
RANGE_MINUTES = 5
# Fixed up front, before any result was seen: large US common stocks as I knew them around 2020, one share class
# each, no ETFs or ADRs, no ticker changes (FB/META, PCLN/BKNG, UTX/RTX, ANTM/ELV). Survivors only: see docs/intraday.md.
CANDIDATES = tuple("""AAPL MSFT AMZN GOOGL JPM JNJ V PG UNH HD MA NVDA DIS BAC VZ ADBE CRM NFLX CMCSA PFE T KO PEP INTC
CSCO XOM MRK WMT ABT TMO CVX MCD NKE ORCL ACN COST AVGO LLY MDT TXN HON QCOM NEE UNP PM IBM LOW AMGN BMY SBUX UPS AMD GS
MS BLK CAT DE MMM GE BA LMT C WFC AXP USB SCHW GILD MO CVS CI MDLZ ISRG TGT F GM TSLA PYPL INTU AMAT MU ADP DHR ABBV BIIB
MET PNC COP SLB EOG OXY TJX LRCX DUK SO CL KMB SPGI AMT ZTS SYK BDX FDX CSX""".split())


def _digest(payload):
    return alpaca_bars._digest(payload)


def _cached(path, build):
    """JSON cache with a sha256 over the payload, rechecked on every read."""
    path = Path(path)
    if path.is_file():
        record = json.loads(path.read_text(encoding="utf-8"))
        if _digest(record["payload"]) != record["sha256"]:
            raise ValueError(f"Cached {path.name} does not match its recorded sha256")
        return record["payload"]
    started = time.time()
    payload, requests = build()
    record = dict(payload=payload, sha256=_digest(payload), requests=requests,
                  fetch_seconds=round(time.time() - started, 1), fetched_at_utc=datetime.now(timezone.utc).isoformat())
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(record), encoding="utf-8")
    temporary.replace(path)
    return payload


def _day(stamp):
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(alpaca_bars.EASTERN).date()


def calendar(start, end, data_dir=DATA):
    """{date: (open_minute, close_minute)} from Alpaca's trading calendar (half days included)."""
    def build():
        entries = alpaca_bars._calendar(start, end, alpaca_bars.credentials())
        return [[e["date"], e["open"], e["close"]] for e in entries], 1
    out = {}
    for day, opening, closing in _cached(Path(data_dir) / f"calendar_{start}_{end}.json", build):
        (oh, om), (ch, cm) = (map(int, x.split(":")) for x in (opening, closing))
        out[date.fromisoformat(day)] = (oh * 60 + om, ch * 60 + cm)
    return out


def daily_bars(symbols, start, end, adjustment, data_dir=DATA, size=25):
    """{symbol: {date: (open, close, volume)}} from SIP 1Day bars. adjustment is 'raw' or 'all'."""
    symbols, out = sorted(set(symbols)), {}
    headers = alpaca_bars.credentials()
    for n in range(0, len(symbols), size):
        group = symbols[n:n + size]
        key = hashlib.sha256("|".join(group).encode()).hexdigest()[:12]

        def build(group=group):
            params = {"symbols": ",".join(group), "timeframe": "1Day", "adjustment": adjustment, "feed": "sip",
                      "limit": 10000, "sort": "asc", "start": f"{start}T00:00:00Z", "end": f"{end}T00:00:00Z"}
            bars, pages = {}, alpaca_bars._pages("/v2/stocks/bars", params, headers)
            for page in pages:
                for symbol, rows in (page.get("bars") or {}).items():
                    bars.setdefault(symbol, []).extend([_day(r["t"]).isoformat(), r["o"], r["c"], r["v"]] for r in rows)
            return bars, len(pages)
        for symbol, rows in _cached(Path(data_dir) / f"daily_{adjustment}_{start}_{end}_{key}.json", build).items():
            out[symbol] = {date.fromisoformat(d): (o, c, v) for d, o, c, v in rows}
    return out


def merge_daily(raw, adj):
    """{symbol: {date: (raw_open, raw_close, raw_volume, adj_open, adj_close)}} on dates present in both."""
    return {s: {d: raw[s][d] + adj[s][d][:2] for d in raw[s].keys() & adj.get(s, {}).keys()} for s in raw}


def monthly_universe(daily, months, n=20, min_share=0.8):
    """{(year, month): top-n symbols by prior-month dollar volume (raw close x raw volume)}.

    A symbol needs bars on at least min_share of the prior month's sessions. Only prior-month data is read.
    """
    sessions = {}
    for rows in daily.values():
        for d in rows:
            sessions.setdefault((d.year, d.month), set()).add(d)
    out = {}
    for year, month in months:
        prior = (year - 1, 12) if month == 1 else (year, month - 1)
        need = min_share * len(sessions.get(prior, ()))
        scores = {}
        for symbol, rows in daily.items():
            days = [d for d in rows if (d.year, d.month) == prior]
            if need and len(days) >= need:
                scores[symbol] = sum(rows[d][1] * rows[d][2] for d in days)
        out[(year, month)] = sorted(sorted(scores), key=lambda s: -scores[s])[:n]
    return out


def overnight_legs(daily, picks, sessions):
    """Legs buying at day t-1's official close and selling at day t's official open, per symbol picked at t-1."""
    legs = {}
    for previous, day in zip(sessions, sessions[1:]):
        for symbol in picks(previous):
            a, b = daily[symbol].get(previous), daily[symbol].get(day)
            if a and b:
                legs.setdefault(day, []).append((symbol, a[1], b[3] / a[4]))
    return legs


def intraday_legs(daily, picks, sessions):
    """The mirror: buy day t's official open, sell its official close, for symbols picked at t-1 (known by the open)."""
    legs = {}
    for previous, day in zip(sessions, sessions[1:]):
        for symbol in picks(previous):
            row = daily[symbol].get(day)
            if row:
                legs.setdefault(day, []).append((symbol, row[0], row[4] / row[3]))
    return legs


def run_legs(legs, sessions, slip_bps, equity=100000.):
    """Equal-weight legs per day. A leg is (symbol, raw entry price, total-return price ratio exit/entry).

    Per-side slippage worsens both fills. Shares are whole, sized from equity before the day's legs, and the day's
    P&L (fees and slippage included) is booked on the day the leg exits.
    """
    s, curve, trades, fee_total, slip_total = slip_bps / 10000, [], [], 0., 0.
    for day in sessions:
        todays, start = legs.get(day, []), equity
        for symbol, price, ratio in todays:
            shares = math.floor(start / len(todays) / (price * (1 + s)))
            if shares < 1:
                continue
            out = price * ratio * (1 - s)
            fee = sum(harness.fees(shares, price * (1 + s))) + sum(harness.fees(-shares, out))
            pnl = shares * (out - price * (1 + s)) - fee
            equity += pnl
            fee_total += fee
            slip_total += shares * price * s + shares * price * ratio * s
            trades.append((day, pnl, pnl / (shares * price)))
        curve.append((day, equity))
    return curve, trades, fee_total + slip_total


def buy_hold(daily, picks, sessions, equity=100000.):
    """Frictionless equal-weight close-to-close total return of the same picks (rebalanced daily)."""
    start, curve = equity, []
    for previous, day in zip(sessions, sessions[1:]):
        r = [daily[s][day][4] / daily[s][previous][4] for s in picks(previous) if day in daily[s] and previous in daily[s]]
        equity *= sum(r) / len(r) if r else 1
        curve.append((day, equity))
    return [(sessions[0], start)] + curve


def yearly(curve, start_equity=100000.):
    out, previous = {}, start_equity
    for i, (day, value) in enumerate(curve):
        if i + 1 == len(curve) or curve[i + 1][0].year != day.year:
            out[day.year] = value / previous - 1
            previous = value
    return out


def metrics(curve, trades=(), cost=0., start_equity=100000., sessions=None):
    """CAGR, Sharpe (252-day, zero risk-free), max drawdown and trade statistics from a daily equity curve."""
    values = [start_equity] + [v for _, v in curve]
    returns = [b / a - 1 for a, b in zip(values, values[1:])]
    years = (curve[-1][0] - curve[0][0]).days / 365.25
    mean = sum(returns) / len(returns)
    sd = (sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)) ** 0.5
    peak, drawdown = values[0], 0.
    for v in values:
        peak = max(peak, v)
        drawdown = min(drawdown, v / peak - 1)
    out = dict(final_equity=values[-1], total_return=values[-1] / start_equity - 1,
               cagr=(values[-1] / start_equity) ** (1 / years) - 1 if values[-1] > 0 else -1.,
               sharpe=mean / sd * 252 ** 0.5 if sd else 0., max_drawdown=drawdown, sessions=len(curve))
    if trades:
        out.update(trades=len(trades), win_rate=sum(t[1] > 0 for t in trades) / len(trades),
                   avg_trade_usd=sum(t[1] for t in trades) / len(trades),
                   avg_trade_bps=sum(t[2] for t in trades) / len(trades) * 10000,
                   trades_per_day=len(trades) / len(curve), cost_usd=cost,
                   cost_drag_pct_per_year=cost / (sum(values) / len(values)) / years * 100)
    return out


# ---- opening-range breakout ------------------------------------------------------------------------------------

def opening_range(bars):
    """(high, low) of the 09:30-09:34 bars, or None unless all five exist. bars are (minute, o, h, l, c)."""
    rng = [b for b in bars if OPEN_MIN <= b[0] < OPEN_MIN + RANGE_MINUTES]
    return (max(b[2] for b in rng), min(b[3] for b in rng)) if len(rng) == RANGE_MINUTES else None


def orb_day(bars, close_minute, slip_bps, allow_short=True):
    """One day for one stock: None, or a trade dict with entry/exit prices per share. No fees, no sizing.

    The trigger is a bar CLOSE through the range, first seen on the 09:35 bar. The fill is the next bar's open
    worsened by slippage. The stop is the opposite side of the range and is checked from the fill bar itself; a bar
    that opens through the stop fills at its open. Exit is the open of the bar at close_minute - 5 (or the last
    bar's close if none). Long-only mode ignores downside breaks and keeps waiting for an upside one.
    """
    rng = opening_range(bars)
    if not rng or rng[0] <= rng[1]:
        return None
    high, low = rng
    s, exit_minute = slip_bps / 10000, close_minute - EXIT_BEFORE_CLOSE
    session = [b for b in bars if OPEN_MIN <= b[0] < close_minute]
    for i, bar in enumerate(session):
        if bar[0] < OPEN_MIN + RANGE_MINUTES or bar[0] >= exit_minute:
            continue
        side = 1 if bar[4] > high else -1 if bar[4] < low and allow_short else 0
        if not side:
            continue
        if i + 1 >= len(session) or session[i + 1][0] >= exit_minute:
            return None
        fill, stop = session[i + 1], low if side > 0 else high
        entry = fill[1] * (1 + s * side)
        if (entry - stop) * side <= 0:
            return None
        for later in session[i + 1:]:
            if later[0] >= exit_minute:
                price, at = later[1] * (1 - s * side), later[0]
                break
            if (later[3] <= stop) if side > 0 else (later[2] >= stop):
                gap = (later[1] <= stop) if side > 0 else (later[1] >= stop)
                price, at = (later[1] if gap else stop) * (1 - s * side), later[0]
                break
        else:
            price, at = session[-1][4] * (1 - s * side), session[-1][0]
        return dict(side=side, minute=fill[0], entry=entry, stop=stop, exit=price, exit_minute=at)
    return None


def size_trades(trades, equity, risk=0.01, leverage=4.):
    """Fixed-risk shares per trade: risk x start-of-day equity / stop distance, capped so that concurrent gross
    notional stays within leverage x equity. trades are (symbol, trade dict); sized in entry order."""
    out, open_ = [], []
    for symbol, t in sorted(trades, key=lambda x: x[1]["minute"]):
        used = sum(n for m, n in open_ if m > t["minute"])
        distance = abs(t["entry"] - t["stop"])
        shares = min(math.floor(risk * equity / distance), math.floor((leverage * equity - used) / t["entry"]))
        if shares < 1:
            continue
        open_.append((t["exit_minute"], shares * t["entry"]))
        out.append((symbol, t, shares))
    return out


def settle(sized):
    """(symbol, net P&L, fees, entry notional, trade) per sized trade; fees are harness.fees on both sides."""
    results = []
    for symbol, t, shares in sized:
        signed = shares * t["side"]
        fee = sum(harness.fees(signed, t["entry"])) + sum(harness.fees(-signed, t["exit"]))
        results.append((symbol, shares * (t["exit"] - t["entry"]) * t["side"] - fee, fee, shares * t["entry"], t))
    return results


# ---- minute-bar fetch for ORB ------------------------------------------------------------------------------------

def _offsets():
    cache = {}

    def offset(day):
        if day not in cache:
            noon = datetime(*map(int, day.split("-")), 12, tzinfo=timezone.utc)
            cache[day] = noon.astimezone(alpaca_bars.EASTERN).utcoffset().total_seconds() // 60
        return cache[day]
    return offset


def month_bars(symbol, year, month, end, sessions, data_dir=DATA):
    """{iso date: [[minute, o, h, l, c], ...]} regular-hours minute bars for one symbol-month (raw SIP)."""
    start = date(year, month, 1)
    stop = min(date(year + (month == 12), month % 12 + 1, 1), end)
    offset = _offsets()

    def build():
        params = {"timeframe": "1Min", "adjustment": "raw", "feed": "sip", "limit": 10000, "sort": "asc",
                  "start": f"{start}T00:00:00Z", "end": f"{stop}T00:00:00Z"}
        pages, days = alpaca_bars._pages(f"/v2/stocks/{symbol}/bars", params, alpaca_bars.credentials()), {}
        for page in pages:
            for r in page.get("bars") or []:
                t = r["t"]
                if not "13" <= t[11:13] <= "21":
                    continue
                minute = int(t[11:13]) * 60 + int(t[14:16]) + offset(t[:10])
                day = date.fromisoformat(t[:10])
                if day in sessions and sessions[day][0] <= minute < sessions[day][1]:
                    days.setdefault(t[:10], []).append([minute, r["o"], r["h"], r["l"], r["c"]])
        return days, len(pages)
    return _cached(Path(data_dir) / "orb" / f"{symbol}_{year}-{month:02d}.json", build)


def prefetch(pairs, end, sessions, workers=4, log=print):
    """Fetch every (symbol, year, month) cache not already on disk, a few threads at a time."""
    todo = [p for p in pairs if not (DATA / "orb" / f"{p[0]}_{p[1]}-{p[2]:02d}.json").is_file()]
    done = 0

    def one(p):
        for attempt in range(6):  # alpaca_bars retries only HTTP 429; a dropped connection raises OSError
            try:
                month_bars(*p[:3], end, sessions)
                return p
            except OSError:
                if attempt == 5:
                    raise
                time.sleep(2 ** attempt)
    with ThreadPoolExecutor(workers) as pool:
        for _ in pool.map(one, todo):
            done += 1
            if done % 50 == 0:
                log(f"orb fetch {done}/{len(todo)}")
    return len(todo)

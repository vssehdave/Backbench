"""Munger-style 200-week moving average: buy high-quality stocks at or below the average, sell X% above it."""
from datetime import date

WEEKS = 200
EXIT_ABOVE = 0.20  # X: hold until price is at least 20% above the 200-week MA (fixed before looking at results)
ROE_MIN, DEBT_EQUITY_MAX, YEARS = 0.15, 1.0, 5


def weekly_ma(dates, prices, weeks=WEEKS):
    """Mean of the last `weeks` weekly closes (last session of each ISO week; the latest close ends the final week).

    Returns None until `weeks` weeks with a price exist.
    """
    closes, week = [], None
    for d, p in zip(dates, prices):
        key = d.isocalendar()[:2]
        if p is None:
            continue
        if key == week:
            closes[-1] = p
        else:
            closes.append(p)
            week = key
    return sum(closes[-weeks:]) / weeks if len(closes) >= weeks else None


def _latest(rows, as_of, end_col=1):
    """One value per period end, from the latest filing with filed <= as_of: {end: value}."""
    out = {}
    for row in sorted(r for r in rows if r[0] <= as_of):  # ISO dates sort by filing date
        out[row[end_col]] = row[-1]
    return out


def high_quality(rec, day):
    """ROE > 15%, debt/equity < 1 and positive earnings in each of the last 5 fiscal years, using filings up to `day`.

    Missing debt tags count as zero debt (a stated bias toward passing); missing earnings or equity fail.
    """
    as_of = str(day)
    income = _latest(rec["ni"], as_of, 2) or _latest(rec["ni2"], as_of, 2)
    if len(income) < YEARS:
        return False
    years = sorted(income)[-YEARS:]
    if (date.fromisoformat(as_of) - date.fromisoformat(years[-1])).days > 460 or min(income[y] for y in years) <= 0:
        return False
    equity = _latest(rec["eq"], as_of) or _latest(rec["eq2"], as_of)
    if years[-1] not in equity or equity[years[-1]] <= 0:
        return False
    if income[years[-1]] / equity[years[-1]] <= ROE_MIN:
        return False
    ltd, ltd_nc = _latest(rec["ltd"], as_of), _latest(rec["ltd_nc"], as_of)
    current = _latest(rec["ltd_c"], as_of) or _latest(rec["debt_c"], as_of)
    end = years[-1]
    if end in ltd:
        debt = ltd[end]
    elif end in ltd_nc:
        debt = ltd_nc[end] + current.get(end, 0.)
    else:
        debt = _latest(rec["ltd_cap"], as_of).get(end, 0.)
    return debt / equity[end] < DEBT_EQUITY_MAX


def make_decide(records, exit_above=EXIT_ABOVE):
    """Stateful strategy: a fresh call per run. records maps symbol -> compact EDGAR record (data/edgar)."""
    held, memo = set(), {}

    def decide(seen, params):
        i = len(seen.dates) - 1
        nxt = {}
        for s, prices in seen.prices.items():
            ma = weekly_ma(seen.dates, prices)
            if ma is None:
                continue
            if s in held:
                if prices[i] < ma * (1 + exit_above):
                    nxt[s] = True
            elif prices[i] <= ma and s in records:
                key = (s, seen.date.year, seen.date.month)  # fundamentals change at most monthly; cache per month
                if key not in memo:
                    memo[key] = high_quality(records[s], seen.date)
                if memo[key]:
                    nxt[s] = True
        held.clear()
        held.update(nxt)
        return {s: 1 / len(held) for s in sorted(held)}
    return decide

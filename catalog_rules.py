"""Rules for the multi-symbol catalog runs (catalog_run.py). hist is {symbol: rows (day, o, h, l, c, v)} up to the last
completed bar; each rule returns {symbol: weight} (1.0 = a 5,000 USD unit). Periodic rules use only data up to the last
month or week end, so the weights are the same on every day of the period and shares are held (no daily trading)."""
import math
from statistics import pstdev

from catalog_run import Rebalance

ETFS = ["SPY", "EFA", "EEM", "TLT", "IEF", "GLD", "DBC", "UUP", "FXE", "USO", "VNQ"]  # stand-ins for futures, see READMEs
SECTORS = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]


def month(day):
    return day.year, day.month


def week(day):
    return day.isocalendar()[:2]


def asof(hist, period):
    """hist cut at the end of the last full period, plus whether the newest bar starts a new period."""
    rows = next(iter(hist.values()))
    if len(rows) < 2:
        return None, False
    now = period(rows[-1][0])
    cut = len(rows) - 1
    while cut > 0 and period(rows[cut - 1][0]) == now:
        cut -= 1
    return {s: r[:cut] for s, r in hist.items()}, period(rows[-2][0]) != now


def periodic(hist, period, weights, need=0):
    """Rebalance on the first bar of a period; between those, repeat the weights so nothing trades."""
    cut, new = asof(hist, period)
    if not cut or len(next(iter(cut.values()))) <= need:
        return None
    w = weights(cut)
    return Rebalance(w) if new and w is not None else w


def ret(rows, n):
    return rows[-1][4] / rows[-1 - n][4] - 1


def vol(rows, n):
    return pstdev(math.log(rows[i][4] / rows[i - 1][4]) for i in range(len(rows) - n, len(rows)))


def normalise(raw, gross=1.0):
    total = sum(abs(v) for v in raw.values())
    return {s: v * gross / total for s, v in raw.items()} if total else {s: 0. for s in raw}


def pivot(hist, level):
    """3.14: long between the pivot and resistance, short between support and the pivot, flat beyond either."""
    (symbol, rows), = hist.items()
    if len(rows) < 2:
        return None
    (_, _, high, low, close, _), price = rows[-2], rows[-1][4]
    centre = (high + low + close) / 3
    resistance, support = 2 * centre - low, 2 * centre - high
    return {symbol: 1. if centre < price < resistance else -1. if support < price < centre else 0.}


def ibs(hist, level):
    """4.4: sell the sector ETF with the highest internal bar strength, buy the lowest (top and bottom decile of 9 = 1)."""
    score = {s: (hist[s][-1][4] - hist[s][-1][3]) / (hist[s][-1][2] - hist[s][-1][3]) for s in SECTORS
             if hist[s][-1][2] > hist[s][-1][3]}
    if len(score) < 2:
        return None
    ranked = sorted(score, key=score.get)
    return {ranked[0]: 1., ranked[-1]: -1.}


def letf(hist, level):
    """4.5: short a 3x and a 3x inverse S&P 500 ETF in equal parts, proceeds in a Treasury ETF (half size: gross cap)."""
    return {"SPXL": -.5, "SPXS": -.5, "SHY": 1.}


def trend_long(hist, level):
    """4.6: cumulative return over level days, positive ones only, weights proportional to it (Eq. 371), monthly."""
    return periodic(hist, month, lambda h: normalise({s: ret(h[s], level) for s in ETFS if ret(h[s], level) > 0}), level)


def vol_carry(hist, level):
    """7.3: short VXX, long VXZ with the hedge ratio from regressing VXX on VXZ returns over level days, monthly."""
    def weights(h):
        x = [h["VXX"][i][4] / h["VXX"][i - 1][4] - 1 for i in range(len(h["VXX"]) - level, len(h["VXX"]))]
        z = [h["VXZ"][i][4] / h["VXZ"][i - 1][4] - 1 for i in range(len(h["VXZ"]) - level, len(h["VXZ"]))]
        mz, mx = sum(z) / level, sum(x) / level
        beta = sum((a - mz) * (b - mx) for a, b in zip(z, x)) / sum((a - mz) ** 2 for a in z)
        return {"VXX": -1., "VXZ": min(max(beta, 0.), 1.)}
    return periodic(hist, month, weights, level)


def hp_trend(values, lam):
    """Hodrick-Prescott trend: solves (I + lam D'D) s = y with D the second difference, by banded elimination."""
    n = len(values)
    u = [[0.] * 3 for _ in range(n)]  # upper band of the symmetric matrix: u[i][d] = A[i][i+d]
    for i in range(n - 2):  # D'D accumulates the outer products of the rows (1, -2, 1)
        for a, ca in enumerate((1., -2., 1.)):
            for b, cb in enumerate((1., -2., 1.)):
                if b >= a:
                    u[i + a][b - a] += lam * ca * cb
    b = list(values)
    for i in range(n):
        u[i][0] += 1.
    for i in range(n):
        for j in range(i + 1, min(i + 3, n)):
            f = u[i][j - i] / u[i][0]
            for k in range(j, min(i + 3, n)):
                u[j][k - j] -= f * u[i][k - i]
            b[j] -= f * b[i]
    x = [0.] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(u[i][d] * x[i + d] for d in (1, 2) if i + d < n)) / u[i][0]
    return x


def fx_hp(hist, level):
    """8.1: MA(10) vs MA(30) of the HP-filtered FXE log price over the last 252 days, lambda = 100 * 252^2; long/short."""
    rows = hist["FXE"]
    if len(rows) < 252:
        return None
    trend = hp_trend([math.log(r[4]) for r in rows[-252:]], 100 * 252 ** 2)
    return {"FXE": 1. if sum(trend[-10:]) / 10 > sum(trend[-30:]) / 30 else -1.}


def trend_futures(hist, level):
    """10.4: weights proportional to sign(R)/sigma over level days, sum |w| = 1, monthly; long/short."""
    return periodic(hist, month, lambda h: normalise(
        {s: (1 if ret(h[s], level) > 0 else -1) / vol(h[s], level) for s in ETFS}), level)


def contrarian_futures(hist, level):
    """10.3: weights -gamma (R_i - R_mean) over the last level days, sum |w| = 1, weekly; dollar-neutral."""
    def weights(h):
        r = {s: ret(h[s], level) for s in ETFS}
        mean = sum(r.values()) / len(r)
        return normalise({s: mean - v for s, v in r.items()})
    return periodic(hist, week, weights, level)


def pair(hist, level):
    """3.8: over the last level days short the pair member with the higher return, buy the other, dollar-neutral, monthly."""
    def weights(h):
        a, b = ret(h["KO"], level), ret(h["PEP"], level)
        return {"KO": -.5 if a > b else .5, "PEP": .5 if a > b else -.5}
    return periodic(hist, month, weights, level)


def bullet(hist, level):
    """5.2: one maturity only, here the 7-10 year Treasury ETF (IEF), held."""
    return periodic(hist, month, lambda h: {"IEF": 1.})


def barbell(hist, level):
    """5.3: two maturities, 1-3 year (SHY) and 20+ year (TLT) Treasury ETFs, equal capital, rebalanced monthly."""
    return periodic(hist, month, lambda h: {"SHY": .5, "TLT": .5})


def ladder(hist, level):
    """5.4: equal capital across the three Treasury ETF maturities (SHY, IEF, TLT), rebalanced monthly; three rungs, not ten."""
    return periodic(hist, month, lambda h: {"SHY": 1 / 3, "IEF": 1 / 3, "TLT": 1 / 3})


D1, D2, D3 = 1.9, 7.4, 17.5  # assumed modified durations of SHY, IEF, TLT (about 2, 8.5 and 25 year bonds' ETFs)


def butterfly_zero_cost(hist, level):
    """5.6: long SHY and TLT, short IEF, dollar-neutral and dollar-duration-neutral (Eqs. 404-405) with P2 = 1."""
    return {"SHY": (D3 - D2) / (D3 - D1), "IEF": -1., "TLT": (D2 - D1) / (D3 - D1)}


def butterfly_fifty_fifty(hist, level):
    """5.7: wings with equal dollar durations (P1 D1 = P3 D3 = 2), body short with P2 D2 = 4; not dollar-neutral."""
    return {"SHY": 2 / D1, "IEF": -4 / D2, "TLT": 2 / D3}


def butterfly_maturity(hist, level):
    """5.8.1: curve-neutral (Eq. 408) with beta = (T2 - T1) / (T3 - T2), assumed T = 2, 8.5, 25; body dollar duration 4."""
    beta = (8.5 - 2) / (25 - 8.5)
    wing3 = 4 / (1 + beta)
    return {"SHY": beta * wing3 / D1, "IEF": -4 / D2, "TLT": wing3 / D3}


def commodity_passive(hist, level):
    """9.3 passive approach: 90% equities (SPY), 10% commodities (DBC), rebalanced monthly. The 90/10 split is assumed."""
    return periodic(hist, month, lambda h: {"SPY": .9, "DBC": .1})


def ma(rows, n):
    return sum(r[4] for r in rows[-n:]) / n


def sector_rotation(hist, level):
    """4.1: long the top and short the bottom of 9 sector ETFs (top and bottom decile rounds to 1) by return over level days, monthly."""
    def weights(h):
        r = sorted(SECTORS, key=lambda s: ret(h[s], level))
        return {r[-1]: .5, r[0]: -.5}
    return periodic(hist, month, weights, level)


def sector_rotation_ma(hist, level):
    """4.1.1: 4.1 with the long only if P > MA(200) and the short only if P < MA(200) (T' = 200, top of the paper's 100-200)."""
    def weights(h):
        r = sorted(SECTORS, key=lambda s: ret(h[s], level))
        top, bottom = r[-1], r[0]
        return {top: .5 if h[top][-1][4] > ma(h[top], 200) else 0., bottom: -.5 if h[bottom][-1][4] < ma(h[bottom], 200) else 0.}
    return periodic(hist, month, weights, max(level, 200))


def sector_rotation_absolute(hist, level):
    """4.1.2: long the top sector ETF if SPY > MA(200), otherwise all funds in gold (GLD, the uncorrelated ETF); long only."""
    def weights(h):
        top = max(SECTORS, key=lambda s: ret(h[s], level))
        return {top: 1.} if h["SPY"][-1][4] > ma(h["SPY"], 200) else {"GLD": 1.}
    return periodic(hist, month, weights, max(level, 200))

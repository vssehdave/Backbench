"""Flexible Asset Allocation (Keller and van Putten 2012), the paper's default RAVC model.

Paper rules used unchanged: 7 assets, top N=3 on L = wR*rank(R) + wV*rank(V) + wC*rank(C) with weights 1, 0.5, 0.5
(rank 1 best: highest return, lowest volatility, lowest average correlation to the other six), each pick with
R < 0 replaced by cash, equal weight, rebalanced monthly, lookback 4 months for all three factors.
"""
import math
import statistics

UNIVERSE = ("VTI", "EFA", "EEM", "SHY", "AGG", "DBC", "VNQ")  # paper: VTSMX, FDIVX, VEIEX, VFISX, VBMFX, QRAAX, VGSIX
CASH = "SHY"  # the paper's cash proxy VFISX is also one of its seven ranked funds
LOOKBACK = 84  # 4 months x 21 sessions; the paper gives months only
N, WR, WV, WC = 3, 1., .5, .5


def _ranks(values, best_high):
    """1 = best. Equal values keep universe order (the paper does not specify a tie rule)."""
    order = sorted(range(len(values)), key=lambda i: (-values[i] if best_high else values[i], i))
    out = [0] * len(values)
    for place, i in enumerate(order):
        out[i] = place + 1
    return out


def _corr(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    sa, sb = math.sqrt(sum((x - ma) ** 2 for x in a)), math.sqrt(sum((x - mb) ** 2 for x in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else 0.


def decide(panel, params=None):
    """Weights for the next session from adjusted closes up to the decision date, or None before 4 months of history."""
    lookback = (params or {}).get("lookback", LOOKBACK)
    series = []
    for s in UNIVERSE:
        p = panel.prices.get(s)
        if p is None or len(p) <= lookback or any(x is None for x in p[-1 - lookback:]):
            return None
        series.append(p[-1 - lookback:])
    r = [p[-1] / p[0] - 1 for p in series]
    daily = [[b / a - 1 for a, b in zip(p, p[1:])] for p in series]
    v = [statistics.stdev(d) for d in daily]
    c = [statistics.fmean(_corr(daily[i], daily[j]) for j in range(len(UNIVERSE)) if j != i) for i in range(len(UNIVERSE))]
    rr, rv, rc = _ranks(r, True), _ranks(v, False), _ranks(c, False)
    loss = [WR * rr[i] + WV * rv[i] + WC * rc[i] for i in range(len(UNIVERSE))]
    best = sorted(range(len(UNIVERSE)), key=lambda i: (loss[i], rr[i], i))[:N]
    weights = {}
    for i in best:
        target = UNIVERSE[i] if r[i] >= 0 else CASH
        weights[target] = weights.get(target, 0.) + 1 / N
    return weights

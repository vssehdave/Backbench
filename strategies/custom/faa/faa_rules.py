"""Flexible Asset Allocation (Keller and van Putten 2012), every model the paper reports.

Default (params None) is the paper's RAVC model: 7 assets, top N=3 on L = wR*rank(R) + wV*rank(V) + wC*rank(C) with
weights 1, 0.5, 0.5 (rank 1 best: highest return, lowest volatility, lowest average correlation to the other six), each
pick with R < 0 replaced by cash, equal weight, rebalanced monthly, lookback 4 calendar months (month-end to month-end
close) for all three factors. Params switch to the paper's other models:
  w_return/w_volatility/w_correlation  factor weights (R only: 1/0/0)
  abs_filter     False turns off the R < 0 -> cash rule (the paper's R-only model)
  form           "rank" (eq. 1/2) or "log" (eq. 3: -L = wR ln(r/rmax) + wV ln(vmin/v) + wC ln((cmin+1)/(c+1)))
  n, lookback_months, lookback (sessions; overrides months), leverage (multiplies every weight)
"""
import math
import statistics

UNIVERSE = ("VTI", "EFA", "EEM", "SHY", "AGG", "DBC", "VNQ")  # paper: VTSMX, FDIVX, VEIEX, VFISX, VBMFX, QRAAX, VGSIX
CASH = "SHY"  # the paper's cash proxy VFISX is also one of its seven ranked funds
DEFAULTS = dict(n=3, w_return=1., w_volatility=.5, w_correlation=.5, lookback_months=4, lookback=None,
                abs_filter=True, form="rank", leverage=1.)


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


def start_index(dates, months):
    """Index of the last session of the month `months` before the decision's month, or None if history is shorter."""
    target = dates[-1].year * 12 + dates[-1].month - 1 - months
    found = None
    for j, d in enumerate(dates):
        if d.year * 12 + d.month - 1 > target:
            break
        found = j
    return found


def factors(panel, p):
    """(r, v, c) over the lookback for UNIVERSE, or None if any series is short or has a gap."""
    n = len(panel.dates)
    j = n - 1 - p["lookback"] if p["lookback"] else start_index(panel.dates, p["lookback_months"])
    if j is None or j < 0:
        return None
    series = []
    for s in UNIVERSE:
        x = panel.prices.get(s)
        if x is None or len(x) != n or any(y is None for y in x[j:]):
            return None
        series.append(x[j:])
    r = [x[-1] / x[0] - 1 for x in series]
    daily = [[b / a - 1 for a, b in zip(x, x[1:])] for x in series]
    v = [statistics.stdev(d) for d in daily]
    c = [statistics.fmean(_corr(daily[i], daily[k]) for k in range(len(UNIVERSE)) if k != i) for i in range(len(UNIVERSE))]
    return r, v, c


def picks(r, v, c, p):
    """Universe indexes of the best N on the loss function, before the cash rule."""
    wr, wv, wc = p["w_return"], p["w_volatility"], p["w_correlation"]
    rr = _ranks(r, True)
    if p["form"] == "log":
        # eq. 3 needs r > 0; r <= 0 scores worst (such a pick would go to cash anyway)
        rmax, vmin, cmin = max(r), min(v), min(c)
        loss = [-(wr * math.log(r[i] / rmax) + wv * math.log(vmin / v[i]) + wc * math.log((cmin + 1) / (c[i] + 1)))
                if r[i] > 0 else math.inf for i in range(len(r))]
    else:
        rv, rc = _ranks(v, False), _ranks(c, False)
        loss = [wr * rr[i] + wv * rv[i] + wc * rc[i] for i in range(len(r))]
    return sorted(range(len(r)), key=lambda i: (loss[i], rr[i], i))[:p["n"]]


def decide(panel, params=None):
    """Weights for the next session from adjusted closes up to the decision date, or None before enough history."""
    p = {**DEFAULTS, **(params or {})}
    f = factors(panel, p)
    if f is None:
        return None
    r = f[0]
    weights = {}
    for i in picks(*f, p):
        target = CASH if p["abs_filter"] and r[i] < 0 else UNIVERSE[i]
        weights[target] = weights.get(target, 0.) + p["leverage"] / p["n"]
    return weights

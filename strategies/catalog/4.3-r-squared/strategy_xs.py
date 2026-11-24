"""4.3 R-squared: sort sector ETFs into quintiles by R^2 of a 4-factor daily regression (252 sessions), then take the
top alpha sub-quintile of the lowest R^2 quintile long and the bottom alpha sub-quintile of the highest R^2 quintile
short, half the book each. Every group is at least one ETF.

PROXY: factors are ETF spreads instead of Fama-French and Carhart: MKT = SPY, SMB = IWM - SPY, HML = IVE - IVW,
MOM = MTUM - SPY. No risk-free rate is subtracted.
"""
LABELS = ["survivorship-biased: today's 11 SPDR sector ETFs, thin universe (about one ETF per leg)",
          "proxy: ETF-mimicking factors (SPY, IWM-SPY, IVE-IVW, MTUM-SPY) instead of Fama-French and Carhart"]


def ols(X, y):
    """Least squares with an intercept: (coefficients, intercept first, and R squared), or (None, None) if singular."""
    rows = [[1.0, *r] for r in X]
    k = len(rows[0])
    A = [[sum(r[i] * r[j] for r in rows) for j in range(k)] + [sum(r[i] * v for r, v in zip(rows, y))] for i in range(k)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(A[r][c]))
        A[c], A[piv] = A[piv], A[c]
        if abs(A[c][c]) < 1e-14:
            return None, None
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(k):
            if r != c:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[c])]
    beta = [A[i][k] for i in range(k)]
    mean = sum(y) / len(y)
    sst = sum((v - mean) ** 2 for v in y)
    sse = sum((v - sum(b * x for b, x in zip(beta, r))) ** 2 for r, v in zip(rows, y))
    return beta, 1 - sse / sst if sst else None


def returns(p, n):
    tail = p[-n - 1:]
    return [b / a - 1 for a, b in zip(tail, tail[1:])] if len(tail) == n + 1 and None not in tail else None


def decide(panel, params):
    window, share = params["window"], params["share"]
    f = {s: returns(panel.aux[s], window) for s in ("SPY", "IWM", "IVE", "IVW", "MTUM")}
    if None in f.values():
        return None
    X = [(m, s - m, v - g, q - m) for m, s, v, g, q in zip(f["SPY"], f["IWM"], f["IVE"], f["IVW"], f["MTUM"])]
    fit = {}
    for s, p in panel.prices.items():
        y = returns(p, window)
        if y:
            beta, r2 = ols(X, y)
            if beta and r2 is not None:
                fit[s] = (r2, beta[0])
    if len(fit) < 4:
        return None
    k = max(1, round(len(fit) * share))  # quintile size
    j = max(1, round(k * share))  # sub-quintile size
    by_r2 = sorted(fit, key=lambda s: (fit[s][0], s))
    long_ = sorted(by_r2[:k], key=lambda s: (fit[s][1], s))[-j:]
    short = sorted(by_r2[-k:], key=lambda s: (fit[s][1], s))[:j]
    if set(long_) & set(short):
        return None
    return {**{s: 0.5 / j for s in long_}, **{s: -0.5 / j for s in short}}

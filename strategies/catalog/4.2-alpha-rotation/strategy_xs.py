"""4.2 alpha rotation: sector momentum rotation (4.1) with the ranking variable replaced by the regression intercept
alpha_i of daily ETF returns on three factors over the last 252 sessions; long the top decile (one ETF, floor of one).

PROXY: the Fama-French factors are not in Alpaca data, so they are replaced by ETF return spreads:
MKT = SPY, SMB = IWM - SPY, HML = IVE - IVW (S&P 500 value minus growth). No risk-free rate is subtracted.
"""
LABELS = ["survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held)",
          "proxy: ETF-mimicking factors (SPY, IWM-SPY, IVE-IVW) instead of Fama-French"]


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
    f = {s: returns(panel.aux[s], window) for s in ("SPY", "IWM", "IVE", "IVW")}
    if None in f.values():
        return None
    X = [(m, s - m, v - g) for m, s, v, g in zip(f["SPY"], f["IWM"], f["IVE"], f["IVW"])]
    alpha = {}
    for s, p in panel.prices.items():
        y = returns(p, window)
        if y:
            beta, _ = ols(X, y)
            if beta:
                alpha[s] = beta[0]
    if not alpha:
        return None
    ranked = sorted(alpha, key=lambda s: (alpha[s], s))
    n = max(1, int(len(ranked) * share))
    return {s: 1 / n for s in ranked[-n:]}

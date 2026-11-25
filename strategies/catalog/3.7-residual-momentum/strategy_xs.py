"""3.7 residual momentum (Blitz et al): 12-1 momentum on the residuals of a 36-month regression, decile long/short.

PROXY: the paper regresses on the Fama-French factors MKT, SMB, HML. The panel has no size or book data, so the
regression uses one factor, the equal-weight average return of the stocks being ranked (an in-universe market).
Months are blocks of 21 sessions. Regression months t = S..S+35 (S = 1), residuals for t = S..S+11 without alpha.
"""
import statistics

LABELS = ["survivorship-biased S&P 500 universe", "proxy: market-only regression (equal-weight universe), no SMB/HML"]
MONTH = 21


def decide(panel, params):
    S, T, W, share = params["S"], params["T"], params["W"], params["share"]
    need = (S + W) * MONTH + 1  # prices at t = 0 .. S+W
    at = lambda p, t: p[-1 - MONTH * t]
    names = [s for s, p in panel.prices.items() if len(p) > need and all(at(p, t) is not None for t in range(S + W + 1))]
    if len(names) < 20:
        return None
    ret = {s: {t: at(panel.prices[s], t) / at(panel.prices[s], t + 1) - 1 for t in range(S, S + W)} for s in names}
    mkt = {t: statistics.fmean(ret[s][t] for s in names) for t in range(S, S + W)}
    mx = statistics.fmean(mkt.values())
    vx = sum((x - mx) ** 2 for x in mkt.values())
    score = {}
    for s in names:
        my = statistics.fmean(ret[s].values())
        beta = sum((mkt[t] - mx) * (ret[s][t] - my) for t in mkt) / vx
        resid = [ret[s][t] - beta * mkt[t] for t in range(S, S + T)]  # alpha excluded, as in eq. 279
        sd = statistics.stdev(resid)
        if sd:
            score[s] = statistics.fmean(resid) / sd
    n = int(len(score) * share)
    if n < 1:
        return None
    ranked = sorted(score, key=lambda s: (score[s], s))
    return {**{s: -0.5 / n for s in ranked[:n]}, **{s: 0.5 / n for s in ranked[-n:]}}

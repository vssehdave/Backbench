"""4.1.2 dual-momentum sector rotation: if the broad index (SPY) is above its MA(T') of daily closes (T' = 200) hold the
top-decile sector ETF by 12-month return, otherwise hold the uncorrelated ETF (GLD; the paper names gold or Treasuries).

GLD is tradable in this universe, so the equal-weight benchmark for this strategy includes it.
"""
LABELS = ["survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held)", "safe asset chosen: GLD"]
MONTH = 21


def decide(panel, params):
    T, ma, share, safe = params["T"] * MONTH, params["ma"], params["share"], params["safe"]
    spy = panel.aux["SPY"]
    if len(spy) <= ma or None in spy[-ma:]:
        return None
    if spy[-1] <= sum(spy[-ma:]) / ma:
        return {safe: 1.0} if panel.prices.get(safe, (None,))[-1] is not None else None
    score = {s: p[-1] / p[-1 - T] - 1 for s, p in panel.prices.items() if s != safe and len(p) > T and p[-1 - T]}
    if not score:
        return None
    ranked = sorted(score, key=lambda s: (score[s], s))
    n = max(1, int(len(ranked) * share))
    return {s: 1 / n for s in ranked[-n:]}

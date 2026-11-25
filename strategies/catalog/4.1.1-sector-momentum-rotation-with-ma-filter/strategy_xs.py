"""4.1.1 sector momentum rotation with an MA filter: the top-decile ETF is bought only if its price is above its
MA(T') of daily closes (T' = 200); otherwise that slot stays in cash. Long-only, same universe as 4.1."""
LABELS = ["survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held)"]
MONTH = 21


def decide(panel, params):
    T, ma, share = params["T"] * MONTH, params["ma"], params["share"]
    score = {s: p[-1] / p[-1 - T] - 1 for s, p in panel.prices.items() if len(p) > max(T, ma) and p[-1 - T]}
    if not score:
        return None
    ranked = sorted(score, key=lambda s: (score[s], s))
    n = max(1, int(len(ranked) * share))
    out = {}
    for s in ranked[-n:]:
        p = panel.prices[s]
        if None not in p[-ma:] and p[-1] > sum(p[-ma:]) / ma:
            out[s] = 1 / n
    return out  # empty means all cash

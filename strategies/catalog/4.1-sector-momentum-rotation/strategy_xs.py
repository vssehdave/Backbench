"""4.1 sector momentum rotation: long the top decile of sector ETFs by trailing cumulative return (eq. 361).

The universe is the 11 SPDR sector ETFs, so a decile is one ETF (floor of one; XLRE and XLC join once they have
history). Long-only, T = 12 months of 21 sessions, no skip; the paper's dollar-neutral variant is not run.
"""
LABELS = ["survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held)"]
MONTH = 21


def decide(panel, params):
    T, share = params["T"] * MONTH, params["share"]
    score = {s: p[-1] / p[-1 - T] - 1 for s, p in panel.prices.items() if len(p) > T and p[-1 - T]}
    if not score:
        return None
    ranked = sorted(score, key=lambda s: (score[s], s))
    n = max(1, int(len(ranked) * share))
    return {s: 1 / n for s in ranked[-n:]}

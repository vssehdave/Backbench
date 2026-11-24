"""3.1 price momentum (Kakushadze and Serur): long the top decile by R_cum (12 months back, skipping the latest month), short the bottom decile, dollar neutral."""
LABELS = ["survivorship-biased S&P 500 universe"]


def decide(panel, params):
    lookback, skip, share = params["lookback"], params["skip"], params["share"]
    scores = {}
    for symbol, p in panel.prices.items():
        if len(p) > lookback and p[-1 - skip] is not None and p[-1 - lookback] is not None:
            scores[symbol] = p[-1 - skip] / p[-1 - lookback] - 1  # eq. 267; lookback = S + T sessions
    n = int(len(scores) * share)
    if n < 1:
        return None
    ranked = sorted(scores, key=lambda s: (scores[s], s))
    return {**{s: -0.5 / n for s in ranked[:n]}, **{s: 0.5 / n for s in ranked[-n:]}}

"""12-1 month price momentum: long the top decile, short the bottom decile, equal weight, dollar neutral."""


def decide(panel, params):
    skip, lookback, share = params["skip"], params["lookback"], params["share"]
    scores = {}
    for symbol, p in panel.prices.items():
        if len(p) > lookback and p[-1 - lookback] is not None and p[-1 - skip] is not None:
            scores[symbol] = p[-1 - skip] / p[-1 - lookback] - 1
    n = int(len(scores) * share)
    if n < 1:
        return None  # not enough history yet; abstain
    ranked = sorted(scores, key=lambda s: (scores[s], s))
    return {**{s: -0.5 / n for s in ranked[:n]}, **{s: 0.5 / n for s in ranked[-n:]}}

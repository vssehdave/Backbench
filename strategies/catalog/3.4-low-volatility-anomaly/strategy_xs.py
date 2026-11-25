"""3.4 low-volatility anomaly: long the lowest-volatility decile, short the highest, dollar neutral, no skip period."""
import statistics

LABELS = ["survivorship-biased S&P 500 universe"]


def decide(panel, params):
    window, share = params["window"], params["share"]
    scores = {}
    for symbol, p in panel.prices.items():
        tail = p[-window - 1:]
        if len(tail) == window + 1 and None not in tail:
            scores[symbol] = statistics.stdev(b / a - 1 for a, b in zip(tail, tail[1:]))
    n = int(len(scores) * share)
    if n < 1:
        return None
    ranked = sorted(scores, key=lambda s: (scores[s], s))
    return {**{s: 0.5 / n for s in ranked[:n]}, **{s: -0.5 / n for s in ranked[-n:]}}

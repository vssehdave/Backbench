"""Low volatility: long-only, equal weight in the quintile with the lowest trailing daily-return volatility."""
import statistics


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
    return {s: 1 / n for s in sorted(scores, key=lambda s: (scores[s], s))[:n]}

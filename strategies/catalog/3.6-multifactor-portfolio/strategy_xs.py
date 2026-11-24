"""3.6 multifactor: average the demeaned ranks of momentum (12-1) and low volatility, long top decile, short bottom.

PROXY: the paper's headline pair is value and momentum; there is no book value in the panel, so value is replaced
by low volatility (price-only). Ties go to the momentum ranking.
"""
import statistics

LABELS = ["survivorship-biased S&P 500 universe", "proxy: momentum + low volatility, value is not available"]


def decide(panel, params):
    lookback, skip, window, share = params["lookback"], params["skip"], params["window"], params["share"]
    mom, vol = {}, {}
    for symbol, p in panel.prices.items():
        tail = p[-window - 1:]
        if len(p) > lookback and p[-1 - skip] is not None and p[-1 - lookback] is not None \
                and len(tail) == window + 1 and None not in tail:
            mom[symbol] = p[-1 - skip] / p[-1 - lookback] - 1
            vol[symbol] = -statistics.stdev(b / a - 1 for a, b in zip(tail, tail[1:]))  # higher is better
    n = int(len(mom) * share)
    if n < 1:
        return None
    rank_m = {s: r for r, s in enumerate(sorted(mom, key=lambda s: (mom[s], s)))}
    rank_v = {s: r for r, s in enumerate(sorted(vol, key=lambda s: (vol[s], s)))}
    score = {s: (rank_m[s] + rank_v[s]) / 2 for s in mom}  # demeaning every rank by the same constant changes nothing
    ranked = sorted(score, key=lambda s: (score[s], rank_m[s], s))
    return {**{s: -0.5 / n for s in ranked[:n]}, **{s: 0.5 / n for s in ranked[-n:]}}

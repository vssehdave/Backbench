"""3.18 stat-arb optimization, eq. 358 (dollar neutral mean-variance weights), sum of |w| = 1.

PROXY: C is diagonal (sample covariance is singular for N > T and a model covariance is not in the panel), so
w_i ~ (E_i - E_bar) / sigma_i^2 with E_bar the 1/sigma^2-weighted mean. E_i is the 12-1 momentum return, one of the
signals the paper names; the paper fixes neither E nor C.
"""
import statistics

LABELS = ["survivorship-biased S&P 500 universe", "proxy: diagonal covariance, momentum as expected return"]


def decide(panel, params):
    lookback, skip, window = params["lookback"], params["skip"], params["window"]
    E, var = {}, {}
    for symbol, p in panel.prices.items():
        tail = p[-window - 1:]
        if len(p) > lookback and p[-1 - skip] is not None and p[-1 - lookback] is not None \
                and len(tail) == window + 1 and None not in tail:
            E[symbol] = p[-1 - skip] / p[-1 - lookback] - 1
            var[symbol] = statistics.variance(b / a - 1 for a, b in zip(tail, tail[1:]))
    if len(E) < 2:
        return None
    mean_e = sum(E[s] / var[s] for s in E) / sum(1 / var[s] for s in E)
    w = {s: (E[s] - mean_e) / var[s] for s in E}
    gross = sum(abs(x) for x in w.values())
    return {s: x / gross for s, x in w.items()} if gross else None

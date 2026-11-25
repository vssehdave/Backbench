"""Signal helpers for lab strategies. seen is an xsection.AsOf: closes up to and including the decision day."""
import math
import statistics


def closes(seen, symbol, n):
    """The last n adjusted closes of symbol, or None with too little history."""
    p = [x for x in seen.prices.get(symbol, ()) if x is not None]
    return p[-n:] if len(p) >= n else None


def sma_ratio(seen, symbol, n):
    """close / n-session simple moving average, or None."""
    p = closes(seen, symbol, n)
    return p and p[-1] / statistics.fmean(p)


def ret(seen, symbol, n):
    """Return over the last n sessions, or None."""
    p = closes(seen, symbol, n + 1)
    return p and p[-1] / p[0] - 1


def vol(seen, symbol, n):
    """Annualized stdev of the last n daily returns, or None."""
    p = closes(seen, symbol, n + 1)
    return p and statistics.stdev([b / a - 1 for a, b in zip(p, p[1:])]) * math.sqrt(252)


def inverse_vol(seen, assets, n):
    """Weights proportional to 1 / n-day vol, summing to 1, or None if any asset lacks history."""
    inv = {}
    for s in assets:
        v = vol(seen, s, n)
        if not v:
            return None
        inv[s] = 1 / v
    return {s: x / sum(inv.values()) for s, x in inv.items()}


def vol_cap(seen, w, n, target):
    """Scale weights w down so the mix's realised vol over the last n sessions is at most target; the rest goes to SHY."""
    if not w:
        return {"SHY": 1.0}
    rets = {}
    for s in w:
        c = closes(seen, s, n + 1)
        rets[s] = [b / a - 1 for a, b in zip(c, c[1:])]
    pv = statistics.stdev([sum(w[s] * rets[s][i] for s in w) for i in range(n)]) * math.sqrt(252)
    k = min(1.0, target / pv) if pv else 1.0
    out = {s: x * k for s, x in w.items()}
    out["SHY"] = out.get("SHY", 0) + 1 - k
    return out

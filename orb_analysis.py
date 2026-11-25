"""Per-stock and per-feature statistics for ORB trades, plus the out-of-sample and chance checks. See docs/orb-top50.md.

A trade is a dict with day (date), symbol, ret (net return on its entry notional), pnl (USD at a fixed notional)
and feature values under f. Everything is stdlib.
"""
import math
import random
from bisect import bisect_right


def mean_t(values):
    """(mean, t-stat) of a list; t is naive (assumes independent trades), so it is overstated across same-day trades."""
    n = len(values)
    if n < 2:
        return (values[0] if values else 0., 0.)
    m = sum(values) / n
    sd = (sum((v - m) ** 2 for v in values) / (n - 1)) ** 0.5
    return m, (m / (sd / n ** 0.5) if sd else 0.)


def stock_stats(trades):
    """{symbol: dict(n, pnl, mean_bps, win_rate, profit_factor, t)} over the trades given."""
    groups = {}
    for t in trades:
        groups.setdefault(t["symbol"], []).append(t)
    out = {}
    for s, ts in groups.items():
        wins = sum(t["pnl"] for t in ts if t["pnl"] > 0)
        losses = -sum(t["pnl"] for t in ts if t["pnl"] < 0)
        mean, t_stat = mean_t([t["ret"] for t in ts])
        out[s] = dict(n=len(ts), pnl=sum(t["pnl"] for t in ts), mean_bps=mean * 1e4, t=t_stat,
                      win_rate=sum(t["pnl"] > 0 for t in ts) / len(ts), profit_factor=wins / losses if losses else math.inf)
    return out


def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    out, i = [0.] * len(values), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2
        i = j + 1
    return out


def spearman(x, y):
    if len(x) < 3:
        return 0.
    a, b = ranks(x), ranks(y)
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    cov = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    va, vb = sum((p - ma) ** 2 for p in a), sum((q - mb) ** 2 for q in b)
    return cov / math.sqrt(va * vb) if va and vb else 0.


def cuts(values, parts):
    """Boundaries that split values into `parts` equal-count groups (parts - 1 numbers)."""
    s = sorted(values)
    return [s[len(s) * k // parts] for k in range(1, parts)]


def group_of(value, bounds):
    return bisect_right(bounds, value)


def variance(values):
    m = sum(values) / len(values)
    return sum((v - m) ** 2 for v in values) / max(len(values) - 1, 1)


def quintiles(trades, feature):
    """Spearman rho of feature vs trade return, and mean return (bps) of the lowest and highest quintile."""
    rows = [(t["f"][feature], t["ret"]) for t in trades if t["f"].get(feature) is not None]
    bounds = cuts([r[0] for r in rows], 5)
    low = [r[1] for r in rows if group_of(r[0], bounds) == 0]
    high = [r[1] for r in rows if group_of(r[0], bounds) == 4]
    diff = sum(high) / len(high) - sum(low) / len(low)
    se = math.sqrt(variance(low) / len(low) + variance(high) / len(high))
    return dict(n=len(rows), rho=spearman([r[0] for r in rows], [r[1] for r in rows]),
                bottom_bps=sum(low) / len(low) * 1e4, top_bps=sum(high) / len(high) * 1e4,
                top_minus_bottom_bps=diff * 1e4, naive_t=diff / se if se else 0.)


def by_category(trades, feature):
    """{category: (trades, mean return bps)} for a categorical feature."""
    groups = {}
    for t in trades:
        groups.setdefault(t["f"][feature], []).append(t["ret"])
    return {k: (len(v), sum(v) / len(v) * 1e4) for k, v in sorted(groups.items())}


def winners_vs_rest(trades, features, top=0.2, min_trades=100):
    """Stocks in the top fraction by total P&L (min_trades or more) against the other eligible stocks.

    Each stock's feature is its mean over its own trades; per feature this gives the median of those means for each
    group and the Spearman rho of stock P&L vs stock feature across all eligible stocks. Sectors are counted per group.
    """
    stats = {s: v for s, v in stock_stats(trades).items() if v["n"] >= min_trades}
    ordered = sorted(stats, key=lambda s: -stats[s]["pnl"])
    winners = set(ordered[:max(1, round(len(ordered) * top))])
    means, sector = {}, {}
    for t in trades:
        if t["symbol"] in stats:
            sector[t["symbol"]] = t["f"].get("sector", "unknown")
            for name in features:
                if t["f"].get(name) is not None:
                    means.setdefault(name, {}).setdefault(t["symbol"], []).append(t["f"][name])

    def median(values):
        s = sorted(values)
        return (s[(len(s) - 1) // 2] + s[len(s) // 2]) / 2 if s else None
    out = dict(winners=[s for s in ordered if s in winners], eligible=len(ordered), features={}, sectors={})
    for name in features:
        m = {s: sum(v) / len(v) for s, v in means.get(name, {}).items()}
        both = sorted(m)
        out["features"][name] = dict(
            winners_median=median([m[s] for s in both if s in winners]), rest_median=median([m[s] for s in both if s not in winners]),
            rho_with_pnl=spearman([stats[s]["pnl"] for s in both], [m[s] for s in both]))
    for s in ordered:
        row = out["sectors"].setdefault(sector[s], [0, 0])
        row[s not in winners] += 1
    return out


def split(trades, first_end):
    """(trades on or before first_end, trades after)."""
    return [t for t in trades if t["day"] <= first_end], [t for t in trades if t["day"] > first_end]


def pick_stocks(first, top=0.2, min_trades=60):
    """Symbols in the top fraction by mean return per trade among stocks with at least min_trades in the first half."""
    stats = {s: v for s, v in stock_stats(first).items() if v["n"] >= min_trades}
    ordered = sorted(stats, key=lambda s: -stats[s]["mean_bps"])
    return ordered[:max(1, round(len(ordered) * top))], stats


def persistence(first, second, top=0.2, min_trades=60):
    """How the stocks picked on the first half did on the second: set vs rest, rank correlation of per-stock means."""
    picked, stats_a = pick_stocks(first, top, min_trades)
    stats_b = stock_stats(second)
    chosen = set(picked)
    inside = [t for t in second if t["symbol"] in chosen]
    rest = [t for t in second if t["symbol"] in stats_a and t["symbol"] not in chosen]
    both = [s for s in stats_a if s in stats_b and stats_b[s]["n"] >= min_trades]
    return dict(picked=sorted(picked), eligible=len(stats_a),
                picked_first_half_bps=sum(stats_a[s]["mean_bps"] for s in picked) / len(picked),
                picked_second_half_bps=mean_t([t["ret"] for t in inside])[0] * 1e4, picked_second_half_trades=len(inside),
                picked_second_half_pnl=sum(t["pnl"] for t in inside),
                rest_second_half_bps=mean_t([t["ret"] for t in rest])[0] * 1e4,
                all_second_half_bps=mean_t([t["ret"] for t in second])[0] * 1e4,
                rank_corr_first_vs_second=spearman([stats_a[s]["mean_bps"] for s in both], [stats_b[s]["mean_bps"] for s in both]),
                stocks_in_rank_corr=len(both))


def feature_rules(first, second, features, parts=3):
    """Top- and bottom-tercile rules per feature. Cut points come from the first half only; both halves are scored."""
    out = []
    for name in features:
        bounds = cuts([t["f"][name] for t in first if t["f"].get(name) is not None], parts)
        for label, wanted in (("top", parts - 1), ("bottom", 0)):
            def pick(ts):
                return [t["ret"] for t in ts if t["f"].get(name) is not None and group_of(t["f"][name], bounds) == wanted]
            x, y = pick(first), pick(second)
            out.append(dict(feature=name, rule=label, first_half_bps=mean_t(x)[0] * 1e4, first_half_n=len(x),
                            second_half_bps=mean_t(y)[0] * 1e4, second_half_n=len(y), second_half_t=mean_t(y)[1]))
    return out


def shuffle_test(trades, first_end, sims=300, seed=1, min_trades=50, top=0.2):
    """Chance baseline. Within each day the returns are reassigned among the stocks that traded that day.

    This keeps every stock's trade count and days, the same-day correlation and the pooled mean, and removes any
    stock-specific edge. Scores the observed data and each shuffle the same way: the count of stocks with t > 2
    (n >= min_trades), the largest t, and the second-half mean (bps) of the first-half top-fraction stocks.
    """
    rng = random.Random(seed)
    symbols = sorted({t["symbol"] for t in trades})
    index = {s: i for i, s in enumerate(symbols)}
    days = {}
    for t in trades:
        days.setdefault(t["day"], []).append(t)
    layout = [([index[t["symbol"]] for t in ts], [t["day"] <= first_end for t in ts]) for ts in days.values()]
    returns = [[t["ret"] for t in ts] for ts in days.values()]

    def score(values):
        k = len(symbols)
        n, s, q, n1, s1, n2, s2 = ([0.] * k for _ in range(7))
        for (ids, firsts), r in zip(layout, values):
            for i, first, x in zip(ids, firsts, r):
                n[i] += 1
                s[i] += x
                q[i] += x * x
                if first:
                    n1[i] += 1
                    s1[i] += x
                else:
                    n2[i] += 1
                    s2[i] += x
        t_stats = []
        for i in range(k):
            if n[i] >= min_trades:
                var = (q[i] - s[i] ** 2 / n[i]) / (n[i] - 1)
                t_stats.append(s[i] / n[i] / math.sqrt(var / n[i]) if var > 0 else 0.)
        eligible = sorted((i for i in range(k) if n1[i] >= 60), key=lambda i: -s1[i] / n1[i])
        chosen = eligible[:max(1, round(len(eligible) * top))]
        later = sum(s2[i] for i in chosen) / max(sum(n2[i] for i in chosen), 1)
        return sum(v > 2 for v in t_stats), max(t_stats), later * 1e4, len(t_stats)

    observed = score(returns)
    shuffled = []
    for _ in range(sims):
        values = []
        for r in returns:
            r = r[:]
            rng.shuffle(r)
            values.append(r)
        shuffled.append(score(values))
    counts, maxima, later = ([x[i] for x in shuffled] for i in range(3))

    def pct(values, p):
        return sorted(values)[min(int(p * len(values)), len(values) - 1)]
    return dict(sims=sims, stocks=len(symbols), stocks_tested=observed[3], observed_count_t_over_2=observed[0],
                chance_count_mean=sum(counts) / sims, chance_count_p95=pct(counts, .95),
                observed_max_t=observed[1], chance_max_t_mean=sum(maxima) / sims, chance_max_t_p95=pct(maxima, .95),
                observed_second_half_bps_of_first_half_picks=observed[2],
                chance_second_half_bps_mean=sum(later) / sims, chance_second_half_bps_p95=pct(later, .95),
                p_value_second_half=sum(x >= observed[2] for x in later) / sims)

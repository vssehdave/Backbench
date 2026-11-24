"""Monte Carlo risk: stationary block bootstrap, path rerun (mode A) and P&L bootstrap (mode B). See docs/monte-carlo.md."""
import copy
import random

PERCENTILES = (5, 50, 95, 99)
EXCEEDANCE = (0.2, 0.3, 0.5)


def stationary_indices(pool, n, mean_block, rng):
    """Politis-Romano: n indices into range(pool). Each step continues the block (wrapping) or, with probability
    1/mean_block, starts a new block at a uniform random index, so block lengths are geometric."""
    if pool < 1 or mean_block < 1:
        raise ValueError("Need a non-empty pool and a mean block length of at least 1")
    p, i, out = 1 / mean_block, rng.randrange(pool), []
    for _ in range(n):
        out.append(i)
        i = rng.randrange(pool) if rng.random() < p else (i + 1) % pool
    return out


def percentile(values, q):
    """Linear-interpolated q-th percentile of an ascending list."""
    k = (len(values) - 1) * q / 100
    lo = int(k)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def curve_stats(curve):
    """(max drawdown as a positive fraction, longest run of sessions below the running peak, terminal return,
    share of sessions below the running peak)."""
    peak, worst, run, longest, below = curve[0], 0., 0, 0, 0
    for v in curve[1:]:
        if v >= peak:
            peak, run = v, 0
        else:
            run += 1
            below += 1
            longest = max(longest, run)
            worst = max(worst, (peak - v) / peak)
    return worst, longest, curve[-1] / curve[0] - 1, below / max(len(curve) - 1, 1)


def summarize(real, sims):
    stats = [curve_stats(c) for c in sims]
    h = curve_stats(real)
    out = dict(paths=len(sims), sessions=len(real) - 1,
               historical=dict(max_drawdown=h[0], longest_underwater_sessions=h[1], terminal_return=h[2],
                               share_of_sessions_underwater=h[3]))
    for i, name in enumerate(("max_drawdown", "longest_underwater_sessions", "terminal_return",
                              "share_of_sessions_underwater")):
        column = sorted(s[i] for s in stats)
        out[name] = {f"p{q}": percentile(column, q) for q in PERCENTILES}
    dd = sorted(s[0] for s in stats)
    out["max_drawdown"]["historical_percentile_rank"] = (
        100 * (sum(x < h[0] for x in dd) + sum(x == h[0] for x in dd) / 2) / len(dd))
    out["max_drawdown"]["prob_exceed"] = {str(level): sum(x > level for x in dd) / len(dd) for level in EXCEEDANCE}
    return out


def pnl_bootstrap(curves, paths, seed, mean_block=20):
    """Mode B. {name: equity curve} of equal length -> {name: summary}. Names share block indices (paired)."""
    n = {len(c) for c in curves.values()}
    if len(n) != 1 or n.pop() < 3 or any(min(c) <= 0 for c in curves.values()):
        raise ValueError("Mode B needs equal-length, positive curves of at least three points")
    steps = {k: [b / a for a, b in zip(c, c[1:])] for k, c in curves.items()}
    length = len(next(iter(steps.values())))
    sims = {k: [] for k in curves}
    for i in range(paths):
        index = stationary_indices(length, length, mean_block, random.Random(f"{seed}:B:{i}"))
        for k, ratios in steps.items():
            path = [1.]
            for j in index:
                path.append(path[-1] * ratios[j])
            sims[k].append(path)
    return {k: summarize(curves[k], sims[k]) for k in curves}


class MonteCarlo:
    """Mode A. Each walk-forward fold hands over a function that re-runs the strategy on a synthetic forward path
    glued at the last real close; folds are chained by return into one out-of-sample curve per path."""

    def __init__(self, paths=1000, seed=0, mean_block=20):
        if paths < 1 or mean_block < 1:
            raise ValueError("paths and mean_block must be at least 1")
        self.paths, self.seed, self.block, self.series = paths, seed, mean_block, {}

    def _stitch(self, name, real, sims):
        stitched = self.series.setdefault(name, ([1.], [[1.] for _ in range(self.paths)]))
        for curve, add in zip((real, *sims), (stitched[0], *stitched[1])):
            scale = add[-1] / curve[0]
            add.extend(max(v * scale, 0.) for v in curve[1:])  # a ruined path stays at zero

    def rows_fold(self, name, k, rows, train, forward, run):
        """Single instrument. rows are (date, open, close); run(rows) -> equity curve starting at the opening equity.
        Bootstraps whole bars (overnight gap and open-to-close move together) from every row loaded."""
        self.rows = rows
        bars = [(rows[j][1] / rows[j - 1][2], rows[j][2] / rows[j][1]) for j in range(1, len(rows))]
        sims = []
        for i in range(self.paths):
            price, path = train[-1][2], []
            for row, j in zip(forward, stationary_indices(len(bars), len(forward), self.block,
                                                          random.Random(f"{self.seed}:{k}:{i}"))):
                opening = price * bars[j][0]
                price = opening * bars[j][1]
                path.append((row[0], opening, price))
            sims.append(run(path))
        self._stitch(name, run(forward), sims)

    def panel_fold(self, k, panel, i0, i1, runs):
        """Cross-section. Forward sessions i0+1..i1 are rebuilt from whole bootstrapped dates, so every stock moves
        together as it did that day. runs = {name: function(panel) -> equity curve}. A stock with no bar on a
        bootstrapped date takes that day's equal-weight mean return."""
        dates, ratio_of = len(panel.dates), {}

        def ratios(j):
            if j not in ratio_of:
                r = {s: v[j] / v[j - 1] for s, v in panel.adj.items() if v[j] is not None and v[j - 1] is not None}
                ratio_of[j] = r, (sum(r.values()) / len(r) if r else 1.)
            return ratio_of[j]

        live = [s for s, v in panel.adj.items() if any(x is not None for x in v[i0 + 1:i1 + 1])]
        sims = {name: [] for name in runs}
        for i in range(self.paths):
            index = stationary_indices(dates - 1, i1 - i0, self.block, random.Random(f"{self.seed}:{k}:{i}"))
            synthetic = copy.copy(panel)
            synthetic.adj, synthetic.raw = dict(panel.adj), dict(panel.raw)
            for s in live:
                real, level = panel.adj[s], panel.adj[s][i0]
                adj, raw = real[:i0 + 1], panel.raw[s][:i0 + 1]
                for step, j in zip(range(i0 + 1, i1 + 1), index):
                    if real[step] is None:
                        adj.append(None)
                        raw.append(None)
                        continue
                    by_symbol, mean = ratios(j + 1)
                    level = real[step] if level is None else level * by_symbol.get(s, mean)
                    adj.append(level)
                    raw.append(panel.raw[s][step] * level / real[step])
                synthetic.adj[s], synthetic.raw[s] = adj, raw
            for name, run in runs.items():
                sims[name].append(run(synthetic))
        for name, run in runs.items():
            self._stitch(name, run(panel), sims[name])

    def summary(self):
        real = {name: s[0] for name, s in self.series.items()}
        return dict(config=dict(paths=self.paths, seed=self.seed, mean_block=self.block),
                    mode_a={name: summarize(s[0], s[1]) for name, s in self.series.items()},
                    # Mode B needs positive equity; a ruined stitched history has no return series to resample.
                    mode_b_on_stitched_history=(pnl_bootstrap(real, self.paths, self.seed, self.block)
                                                if all(min(c) > 0 for c in real.values()) else None))

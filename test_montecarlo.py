import csv
import random
import tempfile
import unittest
from datetime import date
from pathlib import Path

import montecarlo as mc
import report
import xsection as xs
from controls import threshold
from harness import fixture, study
from test_xsection import LOOSE, ZERO, momentum_pick, panel_of, sessions, walk


def clustered(n, seed=1):
    """Log returns whose volatility switches between calm and stormy regimes that persist for about 50 sessions."""
    rng, vol, out = random.Random(seed), 0.005, []
    for _ in range(n):
        if rng.random() < 0.02:
            vol = 0.02 if vol < 0.01 else 0.005
        out.append(rng.gauss(0, vol))
    return out


def lag1(x):
    m = sum(x) / len(x)
    return sum((a - m) * (b - m) for a, b in zip(x, x[1:])) / sum((a - m) ** 2 for a in x)


def resample(r, mean_block, seed=0):
    return [r[i] for i in mc.stationary_indices(len(r), len(r), mean_block, random.Random(seed))]


class Bootstrap(unittest.TestCase):
    def test_same_seed_same_paths_and_other_seed_differs(self):
        run = lambda seed: mc.pnl_bootstrap({"s": [100 + i % 7 + i for i in range(60)]}, 20, seed)["s"]
        self.assertEqual(run(3), run(3))
        self.assertNotEqual(run(3), run(4))

    def test_mean_and_variance_preserved(self):
        r = clustered(30000)
        s = resample(r, 20)
        mean, var = sum(r) / len(r), sum(x * x for x in r) / len(r)
        self.assertAlmostEqual(sum(s) / len(s), mean, delta=0.0005)
        self.assertLess(abs(sum(x * x for x in s) / len(s) / var - 1), 0.1)

    def test_blocks_keep_volatility_clustering_better_than_iid(self):
        r = clustered(30000)
        raw = lag1([abs(x) for x in r])
        block, iid = lag1([abs(x) for x in resample(r, 20)]), lag1([abs(x) for x in resample(r, 1)])
        self.assertGreater(raw, 0.2)
        self.assertLess(abs(iid), 0.05)
        self.assertGreater(block, iid + 0.1)
        self.assertLess(abs(block - raw), abs(iid - raw))

    def test_mean_block_length_is_geometric(self):
        i = mc.stationary_indices(1000000, 20000, 20, random.Random(0))
        starts = 1 + sum(b != a + 1 for a, b in zip(i, i[1:]))
        self.assertAlmostEqual(len(i) / starts, 20, delta=2)

    def test_hand_checked_drawdown_and_time_under_water(self):
        # Peak 120, trough 90: 25%. Below the peak on 90 and 95 (two sessions), new high 130, then 100 (one more).
        dd, longest, terminal, share = mc.curve_stats([100, 120, 90, 95, 130, 100])
        self.assertAlmostEqual(dd, 0.25)
        self.assertEqual(longest, 2)
        self.assertAlmostEqual(share, 3 / 5)
        self.assertAlmostEqual(terminal, 0.0)
        self.assertEqual(mc.percentile([1, 2, 3, 4, 5], 50), 3)
        self.assertAlmostEqual(mc.percentile([0, 10], 99), 9.9)

    def test_real_drawdown_sits_inside_the_simulated_distribution(self):
        curve, level = [100.], 100.
        for r in [1.0004] * 200 + [0.97] * 15 + [1.0004] * 200:
            level *= r
            curve.append(level)
        out = mc.pnl_bootstrap({"s": curve}, 400, 0)["s"]
        h, d = out["historical"]["max_drawdown"], out["max_drawdown"]
        self.assertGreater(h, 0.3)
        self.assertGreater(d["p99"], 0.3)
        self.assertTrue(1 < d["historical_percentile_rank"] < 99, d["historical_percentile_rank"])
        self.assertGreater(d["prob_exceed"]["0.2"], d["prob_exceed"]["0.5"])

    def test_drawdown_spans_fold_boundaries(self):
        engine = mc.MonteCarlo(paths=1)
        engine._stitch("x", [1, 1.5, 1.2], [[1, 1.5, 1.2]])
        engine._stitch("x", [1, 1.0, 0.9], [[1, 1.0, 0.9]])
        real, sims = engine.series["x"]
        # peak 1.5 in fold one, trough 1.2 * 0.9 = 1.08 in fold two; each window alone shows at most 20%
        self.assertAlmostEqual(mc.curve_stats(real)[0], 1 - 1.08 / 1.5)
        self.assertAlmostEqual(mc.curve_stats(sims[0])[0], 1 - 1.08 / 1.5)

    def test_mode_b_rejects_bad_curves(self):
        with self.assertRaises(ValueError):
            mc.pnl_bootstrap({"a": [1, 2, 3], "b": [1, 2]}, 5, 0)
        with self.assertRaises(ValueError):
            mc.pnl_bootstrap({"a": [1, 0, 3]}, 5, 0)


class ModeA(unittest.TestCase):
    def harness_run(self, paths=6, seed=7):
        m = mc.MonteCarlo(paths, seed, 10)
        study(fixture(), lambda h, p: 1, [0], 1, 0, 42, date(2022, 1, 1), date(2023, 1, 1),
              mc=lambda *a: m.rows_fold("s", *a))
        return m.series["s"]

    def test_harness_paths_are_deterministic_and_distinct(self):
        real, sims = self.harness_run()
        self.assertEqual((real, sims), self.harness_run())
        self.assertTrue(all(len(c) == len(real) for c in sims))
        self.assertEqual(len({tuple(c) for c in sims}), 6)

    def test_harness_decisions_ignore_later_bars_of_the_synthetic_path(self):
        captured = {}
        study(fixture(), threshold, [98, 100, 102], 1, 0, 42, date(2022, 1, 1), date(2023, 1, 1),
              mc=lambda fold, r, train, forward, run: captured.update(forward=forward, run=run))
        forward, run = captured["forward"], captured["run"]
        for j in range(5, len(forward), 15):
            day, opening, close = forward[j]
            altered = forward[:j] + [(day, opening, close * 2)] + [(d, o * 2, c * 2) for d, o, c in forward[j + 1:]]
            # Equity through the open of day j depends only on earlier bars; day j's own close moves the mark.
            self.assertEqual(run(forward)[:j + 1], run(altered)[:j + 1])

    def test_panel_paths_keep_the_past_and_move_stocks_together(self):
        dates = sessions(date(2024, 1, 2), 90)
        adj = {s: walk(i, 90) for i, s in enumerate("ABCDE")}
        adj["F"] = [None] * 50 + walk(9, 40)
        panels = []
        m = mc.MonteCarlo(3, 0, 10)
        m.panel_fold(0, panel_of(dates, adj), 40, 80, {"x": lambda p: panels.append(p) or [1., 1.]})
        synthetic = panels[0]
        for s in "ABCDE":
            self.assertEqual(synthetic.adj[s][:41], adj[s][:41])
            self.assertNotEqual(synthetic.adj[s][41:81], adj[s][41:81])
            self.assertLessEqual(len(synthetic.adj[s]), 90)  # nothing after the fold end is kept
        self.assertEqual(synthetic.adj["F"][:50], [None] * 50)
        # Joint dates: some real date reproduces every stock's step on a given synthetic day.
        for k in range(41, 81):
            steps = {s: round(synthetic.adj[s][k] / synthetic.adj[s][k - 1], 9) for s in "ABCDE"}
            self.assertTrue(any(all(round(adj[s][j] / adj[s][j - 1], 9) == steps[s] for s in "ABCDE")
                                for j in range(1, 90)))

    def test_panel_decisions_before_the_glue_date_are_the_real_ones(self):
        dates = sessions(date(2024, 1, 2), 90)
        adj = {s: walk(i, 90) for i, s in enumerate("ABCDE")}
        panel, seen = panel_of(dates, adj), []
        run = lambda p: xs.run_window(p, momentum_pick, None, 5, 80, LOOSE, ZERO, "monthly", 100000.)
        mc.MonteCarlo(2, 1, 10).panel_fold(0, panel, 40, 80, {"x": lambda p: seen.append(run(p)) or [1., 1.]})
        cut = str(dates[40])
        real = [d for d in run(panel)["decisions"] if d[0] <= cut]
        self.assertTrue(real)
        self.assertEqual(real, [d for d in seen[0]["decisions"] if d[0] <= cut])


class Output(unittest.TestCase):
    def test_a_run_writes_the_report_and_trade_logs(self):
        m = mc.MonteCarlo(5, 0, 10)
        a = study(fixture(), threshold, [98, 100, 102], 1, 0, 42, date(2022, 1, 1), date(2023, 1, 1),
                  mc=lambda *x: m.rows_fold("strategy", *x))
        b = study(fixture(), lambda h, p: 1, [0], 1, 0, 42, date(2022, 1, 1), date(2023, 1, 1))
        folds = report.folds_of("harness", dict(config=dict(symbol="SPY"), folds=a), dict(folds=b))
        with tempfile.TemporaryDirectory() as tmp:
            report.write_report(tmp, "harness", "t", dict(folds=a), m.summary()["mode_a"], folds, seed=3)
            names = {p.name for p in Path(tmp).iterdir()}
            for n in ("report.json", "REPORT.md", "trades_all.csv", "trades_best_day.md", "trades_worst_day.md",
                      "trades_random_day.md", "trades_best_day.csv", "trades_worst_day.csv", "trades_random_day.csv"):
                self.assertIn(n, names)
            for n in ("trades_all.csv", "trades_random_day.csv"):
                with open(Path(tmp) / n, newline="") as fh:
                    reader = csv.DictReader(fh)
                    count = len(list(reader))
                self.assertEqual(reader.fieldnames, report.COLUMNS)
                self.assertGreater(count, 0)
            text = (Path(tmp) / "trades_random_day.md").read_text()
            for word in ("P&L", "Benchmark move", "Position before", "Position after"):
                self.assertIn(word, text)
            self.assertIn("Monte Carlo max drawdown", (Path(tmp) / "REPORT.md").read_text())


if __name__ == "__main__":
    unittest.main()

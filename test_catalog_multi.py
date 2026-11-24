import importlib
import unittest
from pathlib import Path
from datetime import date, timedelta

import catalog_rules as r
import catalog_run as run


def bars(closes, start=date(2024, 1, 1)):
    return [(start + timedelta(days=i), c, c * 1.01, c * .99, c, 1000.) for i, c in enumerate(closes)]


class MultiTests(unittest.TestCase):
    def test_every_multi_manifest_loads_and_its_rule_exists(self):
        paths = sorted(p for p in Path("strategies/catalog").glob("*/multi*.json") if ".results" not in p.name)
        self.assertGreaterEqual(len(paths), 17)
        for path in paths:
            with self.subTest(path=str(path)):
                module, name = run.load_manifest(path)["entry"].split(":")
                self.assertTrue(callable(getattr(importlib.import_module(module), name)))

    def test_hp_trend_keeps_a_line_and_smooths_noise(self):
        line = [1. + .1 * i for i in range(50)]
        self.assertTrue(all(abs(a - b) < 1e-6 for a, b in zip(r.hp_trend(line, 1600.), line)))
        noisy = [x + (-1) ** i for i, x in enumerate(line)]
        self.assertLess(max(abs(a - b) for a, b in zip(r.hp_trend(noisy, 1600.)[5:-5], line[5:-5])), .5)

    def test_pivot_uses_previous_bar_only(self):
        rows = bars([100, 100, 103])  # previous bar pivot 100, resistance 101: price 103 is beyond it
        self.assertEqual(r.pivot({"X": rows}, 0), {"X": 0.})
        rows = bars([100, 100, 100.5])
        self.assertEqual(r.pivot({"X": rows}, 0), {"X": 1.})
        self.assertEqual(r.pivot({"X": rows[:1]}, 0), None)

    def test_periodic_holds_inside_a_month_and_rebalances_on_the_first_bar(self):
        rows = bars([100.] * 70)
        seen = [r.periodic({"X": rows[:n]}, r.month, lambda h: {"X": 1.}, 5) for n in range(2, 70)]
        flags = [isinstance(w, run.Rebalance) for w in seen]
        self.assertEqual(sum(flags), 2)  # first bars of February and March
        self.assertIsNone(seen[0])

    def test_replay_buys_at_next_open_and_borrow_charged_on_shorts(self):
        data = {"A": bars([100, 100, 110, 110]), "B": bars([100, 100, 100, 100])}
        state, equity, fills = run.replay(data, lambda h, l: {"A": 1., "B": -1.}, 0,
                                          (10000., {}), {"A": [], "B": []}, 0, short=50)
        self.assertEqual([f["date"] for f in fills], ["2024-01-02", "2024-01-02"])
        self.assertLess(equity[-1], 10000. + 5000 * .1)  # fees and borrow only reduce the gain


if __name__ == "__main__":
    unittest.main()

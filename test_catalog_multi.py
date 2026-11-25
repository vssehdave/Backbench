import importlib
import json
import subprocess
import sys
import tempfile
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

    def test_script_run_resizes_on_rebalance_like_the_imported_module(self):
        # Under `python catalog_run.py` the rules saw a different Rebalance class, so isinstance() was False and nothing re-sized.
        rule = "import catalog_rules\n\ndef rule(hist, level):\n    return catalog_rules.Rebalance({'A': 1.})\n"
        manifest = {"id": "t", "version": "1", "entry": "rebalance_rule:rule", "data": {"kind": "alpaca", "symbols": ["A"]},
                    "calendar": "xnys", "warmup": 1, "levels": [0], "costs": "equity_ibkr", "benchmark": {"A": 1.0}}
        driver = ("import runpy, sys, catalog_data\n"
                  "from datetime import date, timedelta\n"
                  "bar = lambda i: (date(2014, 1, 1) + timedelta(i), 100 + i * .05, 101 + i * .05, 99 + i * .05, 100 + i * .05, 1e3)\n"
                  "catalog_data.alpaca_daily = lambda s, a, b: [bar(i) for i in range(1200)]\n"
                  "sys.argv = ['catalog_run.py', sys.argv[1], '--start', '2016-01-01', '--end', '2017-01-01', '--out', sys.argv[2]]\n"
                  "runpy.run_path('catalog_run.py', run_name='__main__')\n")
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "rebalance_rule.py").write_text(rule)
            Path(tmp, "m.json").write_text(json.dumps(manifest))
            subprocess.run([sys.executable, "-c", driver, str(Path(tmp, "m.json")), str(Path(tmp, "out.json"))],
                           check=True, capture_output=True)
            fold = json.loads(Path(tmp, "out.json").read_text())["folds"][0]
        self.assertGreater(fold["buys"] + fold["sells"], 2)  # more than entry and exit: daily re-sizing happened

if __name__ == "__main__":
    unittest.main()

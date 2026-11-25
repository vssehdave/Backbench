import tempfile
import unittest
from pathlib import Path

import catalog_report as cr


class CatalogReportTests(unittest.TestCase):
    def test_discover_uses_folders_and_manifests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, files in (("3.10-b", ["manifest.json", "manifest_long_short.json"]),
                                ("3.2-a", ["xs_manifest.json", "multi.json", "multi.results.json"]),
                                ("4.1-c", []), ("_benchmarks", ["manifest.json"])):
                (root / name).mkdir()
                if not name.startswith("_"):
                    (root / name / "README.md").write_text(
                        f"# {name.split('-')[0]} Name\n\n- Harness status: **not testable: futures** - x\n")
                for f in files:
                    (root / name / f).write_text("{}")
            runs, skipped = cr.discover(root)
            self.assertEqual([(f.name, m.name, e) for f, m, e in runs],
                             [("3.2-a", "xs_manifest.json", "xsection"), ("3.2-a", "multi.json", "multi"),
                              ("3.10-b", "manifest.json", "harness"), ("3.10-b", "manifest_long_short.json", "harness")])
            self.assertEqual([f.name for f in skipped], ["4.1-c"])
            self.assertEqual(cr.readme(skipped[0]), ("4.1", "Name", "not testable: futures"))

    def test_old_cagr_formats(self):
        self.assertAlmostEqual(cr.old_cagr("xs (trusted): +118.2% (CAGR 16.95%, max DD -20.6%)", 5), 0.1695)
        self.assertAlmostEqual(cr.old_cagr("PROXY; mean 6-month -1.0% vs equal-weight", 5), 0.99 ** 2 - 1)
        self.assertAlmostEqual(cr.old_cagr("21.7% vs B&H 46.8%, cash 0%", 5), 1.217 ** 0.2 - 1)
        self.assertIsNone(cr.old_cagr("", 5))

    def test_old_headlines(self):
        text = ("| 3.11 | [Single MA](3.11-single-moving-average/) | ETFs | tested | 21.7% vs B&H 46.8% |\n"
                "| 3.2 | [Earnings](3.2-earnings-momentum/) | Stocks | not testable: x |  |\n")
        self.assertEqual(cr.old_headlines(text), {"3.11-single-moving-average": "21.7% vs B&H 46.8%"})

    def test_check_fails_loudly(self):
        good = dict(name="x", fills=3, mc_config=dict(start="2017-01-01", end="2026-01-01"),
                    metrics=dict(SPY=dict(max_drawdown=-0.3379)))
        cr.check(good, "harness")
        with self.assertRaises(RuntimeError):
            cr.check(dict(good, fills=0), "harness")
        with self.assertRaises(RuntimeError):
            cr.check(dict(good, metrics=dict(SPY=dict(max_drawdown=-0.2))), "harness")
        cr.check(dict(good, mc_config=dict(start="2024-01-19", end="2026-11-20"),
                      metrics=dict(SPY=dict(max_drawdown=-0.2))), "options")

    def test_ruined_strategy_is_reported_not_bootstrapped(self):
        import mc_runs
        from unittest import mock
        result = dict(manifest=dict(id="x", data=dict(kind="alpaca")))
        fold = dict(dates=["d0", "d1", "d2"], equity=[100., 40., -5.], bench=[100., 101., 102.])
        with mock.patch("catalog_run.run", return_value=result), mock.patch("report.folds_of", return_value=[fold]):
            with self.assertRaisesRegex(mc_runs.Ruined, "d2"):
                mc_runs.run_multi("m.json", None, None, 10, 0, 20.)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "4.5-x" / "results").mkdir(parents=True)
            (root / "4.5-x" / "README.md").write_text("# 4.5 Name\n")
            (root / "4.5-x" / "results" / cr.RUINED).write_text("equity fell\n")
            with mock.patch.object(cr.mc_runs, "BENCHMARK", root / "none.json"):
                missing = cr.write_index([(root / "4.5-x", root / "4.5-x" / "multi.json", "multi")], [], root)
            self.assertEqual(missing, [])
            self.assertIn("ruined (multi): equity fell", (root / "INDEX.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

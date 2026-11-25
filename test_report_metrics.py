import math
import unittest
from datetime import date, timedelta

import report

ROOT252 = math.sqrt(252)


class PerfMetrics(unittest.TestCase):
    def test_sharpe_sortino_drawdown_by_hand(self):
        r = [0.02, -0.01, 0.03, 0.0]  # mean .01, sum of squared deviations 1e-3, downside only -0.01
        m = report.perf_metrics(r)
        self.assertAlmostEqual(m["sharpe"], 0.01 / math.sqrt(1e-3 / 3) * ROOT252)
        self.assertAlmostEqual(m["sortino"], 0.01 / math.sqrt(1e-4 / 4) * ROOT252)  # = 2 * sqrt(252)
        self.assertAlmostEqual(m["volatility"], math.sqrt(1e-3 / 3) * ROOT252)
        self.assertAlmostEqual(report.perf_metrics([.1, -.2, .05])["max_drawdown"], -0.2)
        self.assertAlmostEqual(m["cagr"], (1.02 * .99 * 1.03) ** (252 / 4) - 1)
        self.assertIsNone(m["beta"])

    def test_double_spy_has_beta_two_and_no_alpha(self):
        spy = [0.01, -0.02, 0.015, 0.005, -0.01, 0.02]
        m = report.perf_metrics([2 * b for b in spy], spy)
        self.assertAlmostEqual(m["beta"], 2.)
        self.assertAlmostEqual(m["alpha"], 0., places=12)
        self.assertAlmostEqual(report.perf_metrics([2 * b + 0.001 for b in spy], spy)["alpha"], 0.001 * 252)

    def test_flat_series_has_no_ratios(self):
        m = report.perf_metrics([0., 0., 0.], [0.01, -0.01, 0.02])
        self.assertIsNone(m["sharpe"])
        self.assertIsNone(m["sortino"])
        self.assertAlmostEqual(m["beta"], 0.)

    def test_spy_returns_from_closes(self):
        d0 = date(2024, 1, 2)
        spy = {d0 + timedelta(i): 100. + i for i in range(4)}
        got = report.spy_returns([d0 + timedelta(1), d0 + timedelta(3), d0 + timedelta(10)], spy)
        self.assertEqual(got, [101 / 100 - 1, 103 / 102 - 1, 0.])


if __name__ == "__main__":
    unittest.main()

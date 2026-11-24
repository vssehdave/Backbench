import tempfile
import unittest
from datetime import date
import harness
import money
from test_money import GOOD, write


def bars(*closes):
    return [(date(2024, 1, 1 + i), 100., c) for i, c in enumerate(closes)]


class ShortChecks(unittest.TestCase):
    def test_short_pnl_with_fees_and_borrow(self):
        # Short 10 at the 100 open: proceeds 1000, commission 1, regulatory 10*3e-6 + 1000*2.06e-5.
        # 36500 bps a year is 1% a day: the next row accrues 1% of 10 shares at the 95 close = 9.5.
        (cash, shares), equity, fills = harness.replay(
            bars(100, 95, 90), lambda h, level: -10, 0, (10000., 0), [], short=36500.)
        self.assertEqual(shares, -10)
        self.assertEqual(len(fills), 1)
        self.assertAlmostEqual(cash, 10000 + 1000 - 1 - 0.02063 - 9.5, places=6)
        self.assertAlmostEqual(equity[-1], cash - 900, places=6)
        self.assertAlmostEqual(equity[1], 10000 + 1000 - 1 - 0.02063 - 950, places=6)

    def test_flip_long_to_short_in_one_step(self):
        strategy = lambda h, level: 10 if len(h) < 2 else -10
        (cash, shares), _, fills = harness.replay(bars(100, 100, 100), strategy, 0, (10000., 0), [], short=0.)
        self.assertEqual([f["shares"] for f in fills], [10, -20])
        self.assertEqual(shares, -10)
        # Buy 10: 1000 + 1 + 0.00003. Sell 20: +2000 - 1 - (0.00006 + 2000*2.06e-5).
        self.assertAlmostEqual(cash, 10000 - 1001.00003 + 2000 - 1 - 0.04126, places=6)

    def test_short_rejected_without_opt_in(self):
        with self.assertRaises(ValueError):
            harness.replay(bars(100, 100), lambda h, level: -1, 0, (10000., 0), [])
        with tempfile.TemporaryDirectory() as folder:
            bad = dict(GOOD, borrow_bps_per_year=30)
            with self.assertRaisesRegex(money.ManifestError, "needs allow_short"):
                money.load_manifest(write(folder, bad))
            money.load_manifest(write(folder, dict(GOOD, allow_short=True, borrow_bps_per_year=30)))

    def test_equity_wipeout_forces_close_and_stops_trading(self):
        log = {"abstentions": 0}
        (cash, shares), equity, fills = harness.replay(
            bars(100, 100, 220, 220), lambda h, level: -90, 0, (10000., 0), [], log=log, short=0.)
        self.assertEqual(shares, 0)
        self.assertEqual([f.get("forced", False) for f in fills], [False, True])
        self.assertEqual(log["forced_closes"], 1)
        # Short 90: cash 18998.81433. Cover at 220: 19800 + 1 + 90*3e-6.
        self.assertAlmostEqual(cash, 18998.81433 - 19800 - 1 - 0.00027, places=4)
        self.assertEqual(equity[2:], [cash, cash])


if __name__ == "__main__":
    unittest.main()

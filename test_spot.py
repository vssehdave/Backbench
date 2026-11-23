import unittest
from datetime import timedelta

from spot import Spot, spot_fixture


class SpotTest(unittest.TestCase):
    def test_commission_is_symmetric_bps_of_value(self):
        self.assertAlmostEqual(Spot(26, 1, 10).commission(-1000), 2.6)

    def test_rejects_invalid_assumptions(self):
        for args in [(-1, 1, 10), (26, 0, 10), (26, 1, float("nan"))]:
            with self.assertRaises(ValueError):
                Spot(*args)

    def test_fixture_has_every_calendar_day(self):
        days = [r[0] for r in spot_fixture()]
        self.assertTrue(all(b - a == timedelta(days=1) for a, b in zip(days, days[1:])))
        self.assertTrue(any(d.weekday() >= 5 for d in days))


if __name__ == "__main__":
    unittest.main()

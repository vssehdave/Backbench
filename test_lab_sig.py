import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "strategies" / "lab"))
import sig
import xsection


def seen(**series):
    n = len(next(iter(series.values())))
    return xsection.AsOf(date(2020, 1, 1), tuple(range(n)), {s: tuple(v) for s, v in series.items()})


class LabSig(unittest.TestCase):
    calm = [100 * (1.001 if i % 2 else 0.999) ** i for i in range(30)]
    wild = [100 * (1.03 if i % 2 else 0.97) ** i for i in range(30)]

    def test_inverse_vol_favours_the_calm_asset_and_sums_to_one(self):
        w = sig.inverse_vol(seen(A=self.calm, B=self.wild), ["A", "B"], 20)
        self.assertAlmostEqual(sum(w.values()), 1)
        self.assertGreater(w["A"], w["B"])
        self.assertIsNone(sig.inverse_vol(seen(A=self.calm, B=self.wild), ["A", "B"], 40))

    def test_vol_cap_scales_down_and_parks_the_rest_in_shy(self):
        out = sig.vol_cap(seen(B=self.wild), {"B": 1.0}, 20, 0.10)
        self.assertLess(out["B"], 1.0)
        self.assertAlmostEqual(out["B"] + out["SHY"], 1.0)
        self.assertEqual(sig.vol_cap(seen(B=self.wild), {}, 20, 0.10), {"SHY": 1.0})


if __name__ == "__main__":
    unittest.main()

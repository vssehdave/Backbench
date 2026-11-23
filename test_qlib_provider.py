"""Local binary-provider contract for the optional Qlib adapter."""

import importlib.util
import struct
import tempfile
import unittest
from datetime import date
from pathlib import Path

from controls import threshold
from harness import fixture, qlib_rows, study


def write_mini_provider(root, rows):
    """Encode the daily Qlib calendar, instrument span and unadjusted price fields."""
    (root / "calendars").mkdir()
    (root / "instruments").mkdir()
    feature_dir = root / "features" / "probe"
    feature_dir.mkdir(parents=True)
    (root / "calendars/day.txt").write_text(
        "".join(f"{day.isoformat()}\n" for day, _, _ in rows), encoding="ascii"
    )
    (root / "instruments/all.txt").write_text(
        f"PROBE\t{rows[0][0]}\t{rows[-1][0]}\n", encoding="ascii"
    )
    for column, field in ((1, "open"), (2, "close")):
        # Qlib prepends the starting calendar index to a little-endian float32 array.
        values = [0.0] + [row[column] for row in rows]
        (feature_dir / f"{field}.day.bin").write_bytes(
            struct.pack(f"<{len(values)}f", *values)
        )


class QlibProviderTest(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("qlib"), "install requirements-qlib.txt")
    def test_binary_round_trip_and_walk_forward(self):
        # Quarter-dollar values round-trip through float32 without tolerance.
        expected = [(d, round(o * 4) / 4, round(c * 4) / 4) for d, o, c in fixture()]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mini_provider(root, expected)
            rows = qlib_rows(root, "PROBE", "2022-01-01", "2023-12-31")
            self.assertEqual(rows, expected)
            args = (threshold, [98, 100, 102], 2, 10, 17,
                    date(2022, 1, 1), date(2024, 1, 1))
            self.assertEqual(study(rows, *args), study(expected, *args))
            clipped = qlib_rows(root, "PROBE", "2022-06-29", "2022-07-01")
            self.assertEqual(clipped, [r for r in expected
                             if date(2022, 6, 29) <= r[0] <= date(2022, 7, 1)])


if __name__ == "__main__":
    # Standalone acceptance command must fail when the integration cannot execute.
    if not importlib.util.find_spec("qlib"):
        raise SystemExit("Missing Qlib. Install requirements-qlib.txt in CPython 3.11 x64.")
    unittest.main()

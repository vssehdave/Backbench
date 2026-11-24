import json
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import kraken_bars
import money

DAY = 86400
START = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())


def candle(i, price=100.):
    return [START + i * DAY, str(price + i), "1", "1", str(price + i + 0.5), "1", "1", 1]


def reply(count, skip=()):
    return {"error": [], "result": {"XXBTZUSD": [candle(i) for i in range(count) if i not in skip],
                                    "last": START + (count - 1) * DAY}}


def load(response, now, **kwargs):
    """Run daily_from_kraken against a mocked HTTP reply with the clock at `now` (UTC)."""
    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return now
    with tempfile.TemporaryDirectory() as root, mock.patch.object(kraken_bars, "_get", lambda url: response), \
            mock.patch.object(kraken_bars, "datetime", Clock):
        return kraken_bars.daily_from_kraken("XBTUSD", Path(root), **kwargs)


class KrakenTests(unittest.TestCase):
    now = datetime(2024, 1, 10, 6, tzinfo=timezone.utc)  # candle 9 (Jan 10) is still forming

    def test_parses_rows_drops_open_candle_and_reports_quality(self):
        rows, quality = load(reply(10), self.now)
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[0], (date(2024, 1, 1), 100.0, 100.5))
        self.assertEqual(rows[-1][0], date(2024, 1, 9))
        self.assertEqual((quality["first_date"], quality["last_date"], quality["session_count"],
                          quality["missing_dates"], quality["weekend_sessions"]),
                         ("2024-01-01", "2024-01-09", 9, [], 2))

    def test_gap_raises_unless_allowed(self):
        with self.assertRaisesRegex(ValueError, "2024-01-04"):
            load(reply(10, skip={3}), self.now)
        rows, quality = load(reply(10, skip={3}), self.now, allow_gaps=True)
        self.assertEqual((len(rows), quality["missing_dates"]), (8, ["2024-01-04"]))

    def test_sha_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            with mock.patch.object(kraken_bars, "_get", lambda url: reply(5)):
                kraken_bars.daily_from_kraken("XBTUSD", Path(root), allow_gaps=True)
            (path,) = Path(root).glob("*.json")
            record = json.loads(path.read_text())
            record["response"]["result"]["XXBTZUSD"][0][1] = "1"
            path.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, "sha256"):
                kraken_bars.daily_from_kraken("XBTUSD", Path(root))

    def test_api_error_raises(self):
        with tempfile.TemporaryDirectory() as root, \
                mock.patch.object(kraken_bars, "_get", mock.Mock(side_effect=RuntimeError("Kraken error"))):
            with self.assertRaises(RuntimeError):
                kraken_bars.daily_from_kraken("NOPE", Path(root))


class ManifestTests(unittest.TestCase):
    def manifest(self, **changes):
        m = json.loads(Path("strategies/btc_threshold.json").read_text())
        m.update(changes)
        return m

    def test_btc_manifest_is_valid(self):
        self.assertEqual(money.load_manifest("strategies/btc_threshold.json")["data"]["kind"], "kraken")

    def test_kraken_requires_utc24(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "m.json"
            path.write_text(json.dumps(self.manifest(calendar="xnys")))
            with self.assertRaisesRegex(money.ManifestError, "kraken' is a utc24 source but calendar is 'xnys'"):
                money.load_manifest(path)


if __name__ == "__main__":
    unittest.main()

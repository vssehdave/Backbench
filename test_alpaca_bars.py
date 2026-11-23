import json
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

import alpaca_bars

SECRET = "SECRETVALUE123"
ET = ZoneInfo("America/New_York")


def bar(day, hour, minute, price):
    stamp = datetime(day.year, day.month, day.day, hour, minute, tzinfo=ET).astimezone(timezone.utc)
    return {"t": stamp.strftime("%Y-%m-%dT%H:%M:%SZ"), "o": price, "h": price, "l": price, "c": price + 1}


def session(day, minutes=390, price=100.):
    return [bar(day, 9 + (30 + i) // 60, (30 + i) % 60, price + i / 1000) for i in range(minutes)]


class FakeAlpaca:
    def __init__(self, bars, days, actions=None, page=300, closes=None):
        self.bars, self.actions, self.page, self.calls = bars, actions or {}, page, []
        self.calendar = [{"date": str(d), "open": "09:30", "close": (closes or {}).get(d, "16:00")} for d in days]

    def __call__(self, url, headers):
        self.calls.append(url)
        if "/calendar" in url:
            return self.calendar
        if "corporate-actions" in url:
            return {"corporate_actions": self.actions, "next_page_token": None}
        offset = int(url.split("page_token=")[1].split("&")[0]) if "page_token=" in url else 0
        nxt = offset + self.page
        return {"bars": self.bars[offset:nxt], "symbol": "QQQ",
                "next_page_token": str(nxt) if nxt < len(self.bars) else None}


class AlpacaTests(unittest.TestCase):
    def run_source(self, fake, start, end, **kwargs):
        with tempfile.TemporaryDirectory() as root, \
                mock.patch.object(alpaca_bars, "_get", fake), \
                mock.patch.object(alpaca_bars, "credentials", lambda: {"APCA-API-KEY-ID": "id",
                                                                       "APCA-API-SECRET-KEY": SECRET}):
            result = alpaca_bars.daily_from_alpaca("qqq", start, end, data_dir=root, **kwargs)
            return result, [p.read_text() for p in Path(root).iterdir()]

    def test_pagination_and_dst_aggregation(self):
        # 2022-03-11 is EST and 2022-03-14 is EDT: UTC offsets differ but Eastern sessions align.
        days = [date(2022, 3, 11), date(2022, 3, 14)]
        extended = [bar(days[0], 8, 0, 50.), bar(days[0], 16, 0, 60.)]
        bars = extended[:1] + session(days[0]) + extended[1:] + session(days[1], price=200.)
        fake = FakeAlpaca(bars, days)
        (rows, quality), _ = self.run_source(fake, date(2022, 3, 1), date(2022, 4, 1))
        self.assertGreater(sum("page_token" in c for c in fake.calls), 1)
        self.assertEqual(rows[0], (days[0], 100., 100. + 389 / 1000 + 1))
        self.assertEqual(rows[1][:2], (days[1], 200.))
        self.assertEqual(quality["sessions_short_of_calendar"], [])
        self.assertEqual(quality["adjustment"], "raw")

    def test_short_session_reported(self):
        day = date(2022, 11, 25)
        (rows, quality), _ = self.run_source(FakeAlpaca(session(day, 210), [day]), date(2022, 11, 1), date(2022, 12, 1))
        self.assertEqual(quality["sessions_short_of_calendar"],
                         [{"date": "2022-11-25", "first_minute": 570, "last_minute": 779, "observations": 210,
                           "expected": 390}])

    def test_early_close_ignores_after_hours_prints(self):
        day = date(2022, 11, 25)
        # 210 minutes to 13:00, then prints that must not become the close.
        bars = session(day, 210) + [bar(day, 13, m, 500.) for m in range(0, 30)]
        (rows, quality), _ = self.run_source(FakeAlpaca(bars, [day], closes={day: "13:00"}),
                                             date(2022, 11, 1), date(2022, 12, 1))
        self.assertEqual(rows, [(day, 100., 100. + 209 / 1000 + 1)])
        self.assertEqual(quality["early_closes"], [{"date": "2022-11-25", "close_minute": 780}])
        self.assertEqual(quality["sessions_short_of_calendar"], [])

    def test_calendar_mismatch_rejected(self):
        day, other = date(2022, 3, 14), date(2022, 3, 15)
        with self.assertRaisesRegex(ValueError, "No regular-hours bars"):
            self.run_source(FakeAlpaca(session(day), [day, other]), date(2022, 3, 1), date(2022, 4, 1))
        with self.assertRaisesRegex(ValueError, "not in Alpaca's trading calendar"):
            self.run_source(FakeAlpaca(session(day) + session(other), [day]), date(2022, 3, 1), date(2022, 4, 1))

    def test_split_in_range_rejected_unless_allowed(self):
        split = {"forward_splits": [{"symbol": "QQQ", "ex_date": "2022-03-15", "new_rate": 2, "old_rate": 1}]}
        fake = FakeAlpaca(session(date(2022, 3, 14)), [date(2022, 3, 14)], split)
        with self.assertRaisesRegex(ValueError, "splits"):
            self.run_source(fake, date(2022, 3, 1), date(2022, 4, 1))
        (_, quality), _ = self.run_source(fake, date(2022, 3, 1), date(2022, 4, 1), allow_splits=True)
        self.assertEqual(quality["splits"][0]["ex_date"], "2022-03-15")

    def test_credentials_absent_from_cache_and_quality(self):
        (_, quality), cached = self.run_source(FakeAlpaca(session(date(2022, 3, 14)), [date(2022, 3, 14)]),
                                               date(2022, 3, 1), date(2022, 4, 1))
        self.assertEqual(len(cached), 1)
        self.assertNotIn(SECRET, cached[0] + json.dumps(quality))
        self.assertEqual(json.loads(cached[0])["provenance"]["pages_sha256"], quality["pages_sha256"])

    def test_env_file_fallback(self):
        with tempfile.TemporaryDirectory() as root, mock.patch.dict("os.environ", clear=True):
            env = Path(root) / ".env"
            env.write_text(f"APCA_API_KEY_ID=abc\nAPCA_API_SECRET_KEY='{SECRET}'\n")
            self.assertEqual(alpaca_bars.credentials(env)["APCA-API-SECRET-KEY"], SECRET)


if __name__ == "__main__":
    unittest.main()

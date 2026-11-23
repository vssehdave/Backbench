import tempfile
import unittest
from datetime import date
from pathlib import Path

from minute_bars import daily_from_minutes


class MinuteSourceTests(unittest.TestCase):
    def test_date_and_symbol_filter_preserves_first_open_last_close(self):
        with tempfile.TemporaryDirectory() as root:
            file = Path(root) / "bars.csv"
            file.write_text("Date,Symbol,Open,High,Low,Close,Volume\n"
                            "1/4/2016 9:29,QQQ,80,81,80,81,9\n"
                            "1/4/2016 9:30,QQQ,90,92,90,91,1\n"
                            "1/4/2016 9:31,QQQ,91,95,91,95,2\n"
                            "1/4/2016 9:32,OTHER,30,31,30,31,1\n", encoding="ascii")
            rows, quality = daily_from_minutes(file, "QQQ", date(2016,1,1), date(2017,1,1))
            self.assertEqual(rows, [(date(2016,1,4), 90., 95.)])
            self.assertEqual(quality["sessions_under_390"][0]["observations"], 2)
            with file.open("a") as stream:
                stream.write("1/4/2016 9:31,QQQ,91,95,91,95,2\n")
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                daily_from_minutes(file, "QQQ", date(2016,1,1), date(2017,1,1))

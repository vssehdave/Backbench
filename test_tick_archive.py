import gzip
import hashlib
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tick_archive import DAY_NS, database, download_day


class TickArchiveChecks(unittest.TestCase):
    day = date(2016, 1, 4)
    stamp = (day - date(1970, 1, 1)).days * DAY_NS + 123456789

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.db = database(Path(temp.name) / "ticks.db")
        self.addCleanup(self.db.close)

    def test_interruption_resumes_without_duplicates_or_keys(self):
        record = {"sip_timestamp": self.stamp, "sequence_number": 1, "price": 100, "size": 25}
        seen = []
        def fetch(url):
            seen.append(url)
            if len(seen) == 1:
                return {"status": "OK", "results": [record],
                        "next_url": "https://api.massive.com/v3/trades/QQQ?cursor=abc&apiKey=private-test"}
            if len(seen) == 2:
                raise TimeoutError
            return {"status": "OK", "results": [dict(record, sequence_number=2)]}
        with self.assertRaises(TimeoutError):
            download_day(self.db, "QQQ", "trades", self.day, fetch)
        for _ in range(2):
            self.assertEqual(download_day(self.db, "QQQ", "trades", self.day, fetch), 2)
        self.assertEqual(seen[1:], ["https://api.massive.com/v3/trades/QQQ?cursor=abc"] * 2)
        stored = []
        for url, digest, payload in self.db.execute("SELECT source_url,sha256,payload FROM pages ORDER BY page"):
            self.assertNotIn("private-test", url)
            raw = gzip.decompress(payload)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
            stored.extend(json.loads(raw))
        self.assertEqual([r["sequence_number"] for r in stored], [1, 2])
        self.assertEqual(stored[0]["sip_timestamp"], self.stamp)

    def test_empty_quotes_and_rejected_responses(self):
        def run(reply):
            return download_day(self.db, "QQQ", "quotes", self.day, lambda url: reply)
        for reply in [{"status": "NOT_AUTHORIZED"},
                      {"status": "OK", "next_url": "https://example.net/v3/quotes/QQQ"},
                      {"status": "OK", "results": [{"sip_timestamp": self.stamp + DAY_NS}]}]:
            with self.assertRaises(ValueError):
                run(reply)
        self.assertEqual(self.db.execute("SELECT count(*) FROM pages").fetchone(), (0,))
        self.assertEqual(run({"status": "OK", "results": []}), 0)
        self.assertEqual(self.db.execute("SELECT next_url,records FROM partitions").fetchone(), (None, 0))

    def test_quotes_preserved_and_separate_from_trades(self):
        quote = {"sip_timestamp": self.stamp, "bid_price": 100, "ask_price": 100.02, "bid_size": 2}
        download_day(self.db, "QQQ", "quotes", self.day, lambda _: {"status":"OK", "results":[quote]})
        download_day(self.db, "QQQ", "trades", self.day, lambda _: {"status":"OK", "results":[]})
        raw, = self.db.execute("SELECT payload FROM pages WHERE kind='quotes'").fetchone()
        self.assertEqual(json.loads(gzip.decompress(raw)), [quote])

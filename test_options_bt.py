import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

import options_bt as ob
import options_data as od

J19, J22, F16, F20, M15 = date(2024, 1, 19), date(2024, 1, 22), date(2024, 2, 16), date(2024, 2, 20), date(2024, 3, 15)


def fake(closes, call_bars, put_bars=None):
    """Chains of $5 strikes; every symbol is its type and strike, bars come from the dict by (type, strike, expiry)."""

    def contracts(expiry, kind, low, high):
        return {float(k): f"{kind}|{k}|{expiry}" for k in range(300, 700, 5)}

    def bars(symbol, start, end):
        kind, strike, expiry = symbol.split("|")
        return (call_bars if kind == "call" else put_bars or {}).get((float(strike), date.fromisoformat(expiry)), {})
    return contracts, bars


# 500 spot, $100k capital: 2 lots, 200 shares, 2 contracts, no idle cash.
class OptionsBacktest(unittest.TestCase):
    def one(self, strategy, final, bar, key):
        closes = {J19: 500.0, F16: final}
        bars = {key: {J19: bar}}
        c, b = fake(closes, bars if strategy == "covered_call" else {}, bars if strategy == "protective_put" else {})
        return ob.run(strategy, closes, [J19, F16], c, b, half_spread=0.10)

    def test_covered_call_itm_is_assigned(self):
        # Sell 2 x 510C at 4.00 - 0.10 = 3.90: +780.00 - 1.30 fee = 778.70. S=520: pay 10 * 200 = 2000.
        r = self.one("covered_call", 520.0, 4.0, (510.0, F16))
        self.assertAlmostEqual(r["summary"]["end_equity"], 104000 + 778.70 - 2000)
        self.assertEqual((r["summary"]["assignments"], r["summary"]["itm_expiries"]), (1, 1))
        self.assertAlmostEqual(r["summary"]["fees"], 1.30)
        self.assertAlmostEqual(r["buy_and_hold"]["end_equity"], 104000)

    def test_covered_call_otm_expires_worthless(self):
        r = self.one("covered_call", 505.0, 4.0, (510.0, F16))
        self.assertAlmostEqual(r["summary"]["end_equity"], 101000 + 778.70)
        self.assertEqual(r["summary"]["assignments"], 0)

    def test_protective_put_itm_pays_intrinsic(self):
        # Buy 2 x 475P at 2.00 + 0.10: -420.00 - 1.30. S=450: receive 25 * 200 = 5000.
        r = self.one("protective_put", 450.0, 2.0, (475.0, F16))
        self.assertAlmostEqual(r["summary"]["end_equity"], 90000 - 421.30 + 5000)
        self.assertEqual(r["summary"]["assignments"], 0)

    def test_protective_put_otm_expires_worthless(self):
        r = self.one("protective_put", 480.0, 2.0, (475.0, F16))
        self.assertAlmostEqual(r["summary"]["end_equity"], 96000 - 421.30)

    def test_roll_picks_new_strike_from_new_spot(self):
        closes = {J19: 500.0, F16: 520.0, M15: 510.0}
        bars = {(510.0, F16): {J19: 4.0}, (530.0, M15): {F16: 3.0}}  # 520 * 1.02 = 530.4 -> 530
        c, b = fake(closes, bars)
        r = ob.run("covered_call", closes, [J19, F16, M15], c, b, half_spread=0.10)
        self.assertEqual([x["strike"] for x in r["cycles"]], [510.0, 530.0])
        # cycle 1 nets 778.70 - 2000; cycle 2 sells at 2.90: +580 - 1.30, expires OTM at 510.
        self.assertAlmostEqual(r["summary"]["end_equity"], 102000 + 778.70 - 2000 + 578.70)
        self.assertAlmostEqual(r["summary"]["fees"], 2.60)

    def test_missing_bar_days_are_counted_and_entry_slips(self):
        closes = {J19: 500.0, J22: 502.0, F16: 505.0}
        c, b = fake(closes, {(510.0, F16): {J22: 4.0}})
        r = ob.run("covered_call", closes, [J19, F16], c, b, half_spread=0.10)
        self.assertEqual((r["summary"]["no_bar_days"], r["cycles"][0]["entry_fill_date"]), (1, str(J22)))
        closes = {J19: 500.0, J22: 502.0, F16: 505.0}
        c, b = fake(closes, {})
        r = ob.run("covered_call", closes, [J19, F16], c, b)
        self.assertEqual((r["summary"]["no_bar_days"], r["summary"]["cycles_opened"]), (2, 0))
        self.assertAlmostEqual(r["summary"]["end_equity"], 101000)  # unhedged: no premium, no fee

    def test_holiday_friday_expires_the_day_before(self):
        self.assertEqual(ob.third_friday(2024, 2), F16)
        self.assertEqual(ob.monthly_expiries({date(2026, 6, 18)}, date(2026, 6, 1), date(2026, 6, 30)),
                         [date(2026, 6, 18)])


class CacheChecks(unittest.TestCase):
    def test_tampered_cache_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.json"
            pages = [{"bars": {"S": [{"t": "2024-01-18T05:00:00Z", "c": 1.5}]}}]
            with mock.patch("alpaca_bars.credentials", return_value={}):
                got = od._cached(path, {}, lambda h: pages)
                self.assertEqual(got, pages)
                self.assertEqual(od._cached(path, {}, lambda h: self.fail("refetched")), pages)
                record = json.loads(path.read_text())
                record["pages"][0]["bars"]["S"][0]["c"] = 9.9
                path.write_text(json.dumps(record))
                with self.assertRaises(ValueError):
                    od._cached(path, {}, lambda h: pages)


if __name__ == "__main__":
    unittest.main()

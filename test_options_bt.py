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
        self.assertEqual([x["legs"][0]["strike"] for x in r["cycles"]], [510.0, 530.0])
        # cycle 1 nets 778.70 - 2000; cycle 2 sells at 2.90: +580 - 1.30, expires OTM at 510.
        self.assertAlmostEqual(r["summary"]["end_equity"], 102000 + 778.70 - 2000 + 578.70)
        self.assertAlmostEqual(r["summary"]["fees"], 2.60)

    def test_missing_bar_days_are_counted_and_entry_slips(self):
        closes = {J19: 500.0, J22: 502.0, F16: 505.0}
        c, b = fake(closes, {(510.0, F16): {J22: 4.0}})
        r = ob.run("covered_call", closes, [J19, F16], c, b, half_spread=0.10)
        self.assertEqual((r["summary"]["no_bar_days"], r["cycles"][0]["legs"][0]["entry_fill_date"]), (1, str(J22)))
        closes = {J19: 500.0, J22: 502.0, F16: 505.0}
        c, b = fake(closes, {})
        r = ob.run("covered_call", closes, [J19, F16], c, b)
        self.assertEqual((r["summary"]["no_bar_days"], r["summary"]["cycles_opened"]), (2, 0))
        self.assertAlmostEqual(r["summary"]["end_equity"], 101000)  # unhedged: no premium, no fee

    def multi(self, name, final, calls=None, puts=None, expiries=(J19, F16), closes=None):
        closes = closes or {J19: 500.0, F16: final}
        c, b = fake(closes, calls or {}, puts or {})
        return ob.run(name, closes, list(expiries), c, b, half_spread=0.10)

    def test_bull_call_spread_payoff(self):
        # Long 500C at 12.00 + 0.10, short 510C (512.5 ties to the lower strike) at 7.00 - 0.10: net debit 5.20 x 200 = 1040,
        # fees 2 legs x 2 contracts x 0.65 = 2.60. S=520 pays 20 x 200 on the long, owes 10 x 200 on the short.
        r = self.multi("bull_call_spread", 520.0, {(500.0, F16): {J19: 12.0}, (510.0, F16): {J19: 7.0}})
        self.assertAlmostEqual(r["summary"]["end_equity"], 100000 - 1040 - 2.60 + 4000 - 2000)
        self.assertEqual((r["summary"]["itm_expiries"], r["summary"]["assignments"]), (2, 1))
        self.assertAlmostEqual(r["summary"]["fees"], 2.60)

    def test_short_straddle_assigns_the_itm_leg_only(self):
        # Sell 500C at 8.00 - 0.10 and 500P at 7.00 - 0.10: credit 14.80 x 200 = 2960, fees 2.60. S=480: put owes 20 x 200.
        r = self.multi("short_straddle", 480.0, {(500.0, F16): {J19: 8.0}}, {(500.0, F16): {J19: 7.0}})
        self.assertAlmostEqual(r["summary"]["end_equity"], 100000 + 2960 - 2.60 - 4000)
        self.assertEqual((r["summary"]["itm_expiries"], r["summary"]["assignments"]), (1, 1))

    def test_ratio_spread_fees_are_per_contract(self):
        # Long 1 x 485C (487.5 ties down) at 20.10, short 2 x 500C at 7.90: -4020 + 3160. Fees 0.65 x (1 + 2) x 2 = 3.90.
        # S=505: long pays 20 x 200 = 4000, the two shorts owe 2 x 5 x 200 = 2000.
        r = self.multi("ratio_call_spread", 505.0, {(485.0, F16): {J19: 20.0}, (500.0, F16): {J19: 8.0}})
        self.assertAlmostEqual(r["summary"]["fees"], 3.90)
        self.assertAlmostEqual(r["summary"]["end_equity"], 100000 - 4020 + 3160 - 3.90 + 4000 - 2000)

    def test_calendar_far_leg_is_closed_at_the_near_expiry(self):
        # Long 500C (Mar) at 10.10, short 500C (Feb) at 5.90: -840, fees 2.60. At Feb 16 the short owes 5 x 200 = 1000
        # and the long is sold at its 9.00 bar - 0.10 = 8.90 x 200 = 1780 with a 1.30 fee. The Mar expiry only supplies the far leg.
        r = self.multi("calendar_call_spread", 505.0, {(500.0, M15): {J19: 10.0, F16: 9.0}, (500.0, F16): {J19: 6.0}},
                       expiries=(J19, F16, M15))
        self.assertAlmostEqual(r["summary"]["end_equity"], 100000 - 840 - 2.60 - 1000 + 1780 - 1.30)
        self.assertAlmostEqual(r["summary"]["fees"], 3.90)
        self.assertEqual(r["summary"]["cycles"], 1)

    def test_one_missing_leg_skips_the_whole_cycle(self):
        r = self.multi("bull_call_spread", 520.0, {(500.0, F16): {J19: 12.0}})
        self.assertEqual((r["summary"]["cycles_opened"], r["summary"]["fees"]), (0, 0.0))
        self.assertAlmostEqual(r["summary"]["end_equity"], 100000)

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

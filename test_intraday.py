import tempfile
import unittest
from datetime import date
from pathlib import Path

import intraday as I


def bars(spec, start=570):
    """Bars from (o, h, l, c) tuples, one per minute from start."""
    return [(start + i, *x) for i, x in enumerate(spec)]


# 09:30-09:34 range: high 101, low 99.
RANGE = [(100, 101, 99, 100)] * 4 + [(100, 100.5, 99.5, 100)]
FLAT = (100, 100.5, 99.5, 100)


def day(after):
    return bars(RANGE + after)


class RangeTests(unittest.TestCase):
    def test_range_is_first_five_minutes_only(self):
        spec = RANGE + [(100, 105, 90, 100)]
        self.assertEqual(I.opening_range(bars(spec)), (101, 99))

    def test_incomplete_range_gives_no_trade(self):
        self.assertIsNone(I.opening_range(bars(RANGE[:4])))
        self.assertIsNone(I.orb_day(bars(RANGE[:4] + [(102, 103, 101, 102)] * 30), 960, 0))


class BreakoutTests(unittest.TestCase):
    def test_fill_is_next_bar_open_plus_slippage_not_range_price(self):
        # The 09:35 bar closes above 101; the fill is the 09:36 open, 101.4, plus 10 bps.
        t = I.orb_day(day([(100.5, 101.6, 100.4, 101.5), (101.4, 102, 101.3, 101.8)] + [(101.8, 102, 101.7, 101.8)] * 5),
                      960, 10)
        self.assertEqual((t["side"], t["minute"]), (1, 576))
        self.assertAlmostEqual(t["entry"], 101.4 * 1.001)
        self.assertEqual(t["stop"], 99)

    def test_a_wick_above_the_range_without_a_close_is_not_a_signal(self):
        self.assertIsNone(I.orb_day(day([(100, 103, 100, 100.9)] * 30), 960, 0))

    def test_short_break_and_long_only(self):
        spec = [(99.5, 99.6, 98.5, 98.8), (98.7, 98.9, 98.5, 98.6)] + [(98.6, 98.7, 98.5, 98.6)] * 5
        t = I.orb_day(day(spec), 960, 0)
        self.assertEqual((t["side"], t["entry"], t["stop"]), (-1, 98.7, 101))
        self.assertIsNone(I.orb_day(day(spec), 960, 0, allow_short=False))

    def test_one_trade_per_day_first_break_only(self):
        spec = [(100.5, 101.6, 100.4, 101.5), (101.4, 101.5, 101.3, 101.4), (101, 101, 98, 98.5)] + [(98.5, 98.6, 98.4, 98.5)] * 3
        t = I.orb_day(day(spec), 960, 0)
        self.assertEqual(t["side"], 1)

    def test_no_entry_when_breakout_is_too_late_to_fill_before_exit(self):
        spec = [FLAT] * 379 + [(100, 102, 100, 101.5)] * 6  # first close above the range at 15:54
        self.assertIsNone(I.orb_day(day(spec), 960, 0))


class ExitTests(unittest.TestCase):
    ENTRY = [(100.5, 101.6, 100.4, 101.5), (101.4, 101.6, 101.2, 101.5)]

    def test_stop_at_opposite_side_of_range(self):
        t = I.orb_day(day(self.ENTRY + [(101.5, 101.6, 98.8, 99.2)]), 960, 0)
        self.assertEqual((t["exit"], t["exit_minute"]), (99, 577))

    def test_gap_through_stop_fills_at_open_not_stop(self):
        t = I.orb_day(day(self.ENTRY + [(98.0, 98.5, 97.5, 98.2)]), 960, 0)
        self.assertEqual(t["exit"], 98.0)

    def test_stop_can_fire_on_the_fill_bar(self):
        t = I.orb_day(day([(100.5, 101.6, 100.4, 101.5), (101.4, 101.5, 98.9, 99.5)]), 960, 0)
        self.assertEqual((t["minute"], t["exit_minute"], t["exit"]), (576, 576, 99))

    def test_short_stop_and_slippage_worsen_exit(self):
        spec = [(99.5, 99.6, 98.5, 98.8), (98.7, 98.9, 98.5, 98.6), (98.6, 101.5, 98.5, 101.2)]
        t = I.orb_day(day(spec), 960, 100)
        self.assertAlmostEqual(t["entry"], 98.7 * 0.99)
        self.assertAlmostEqual(t["exit"], 101 * 1.01)

    def test_end_of_day_exit_is_the_1555_bar_open(self):
        after = [(100.5, 101.6, 100.4, 101.5)] + [(101.5, 101.8, 101.4, 101.6)] * 379  # 09:35 .. 15:54
        after += [(102.0, 102.1, 101.9, 102.05)] * 5  # 15:55 .. 15:59
        t = I.orb_day(bars(RANGE + after), 960, 0)
        self.assertEqual((t["exit"], t["exit_minute"]), (102.0, 955))

    def test_half_day_exits_at_1255_and_ignores_bars_after_the_close(self):
        after = [(100.5, 101.6, 100.4, 101.5)] + [(101.5, 101.8, 101.4, 101.6)] * 199  # 09:35 .. 12:54
        after += [(103.0, 103.1, 102.9, 103.05)] * 5 + [(50, 51, 49, 50)] * 10  # 12:55 .. 13:04
        t = I.orb_day(bars(RANGE + after), 780, 0)  # calendar close 13:00
        self.assertEqual((t["exit"], t["exit_minute"]), (103.0, 775))

    def test_without_an_exit_bar_the_last_close_is_used(self):
        t = I.orb_day(day(self.ENTRY + [(101.5, 101.9, 101.4, 101.7)]), 960, 0)
        self.assertEqual((t["exit"], t["exit_minute"]), (101.7, 577))


class SizingTests(unittest.TestCase):
    def trade(self, minute, exit_minute, entry=100., stop=99.):
        return dict(side=1, minute=minute, entry=entry, stop=stop, exit=entry, exit_minute=exit_minute)

    def test_risk_sizing_then_leverage_cap(self):
        (_, _, shares), = I.size_trades([("A", self.trade(580, 900))], 100000., risk=0.01, leverage=4.)
        self.assertEqual(shares, 1000)  # 1000 USD risk over 1.00 per share
        (_, _, shares), = I.size_trades([("A", self.trade(580, 900, stop=99.99))], 100000., risk=0.01, leverage=4.)
        self.assertEqual(shares, 4000)  # capped at 4x equity / price

    def test_concurrent_gross_is_capped_and_freed_on_exit(self):
        first, second, third = (self.trade(580, 900, stop=99.99), self.trade(590, 900, stop=99.99),
                                self.trade(950, 955, stop=99.99))
        sized = I.size_trades([("A", first), ("B", second), ("C", third)], 100000., leverage=1.)
        self.assertEqual([(s, n) for s, _, n in sized], [("A", 1000), ("C", 1000)])

    def test_settle_includes_fees_and_sign(self):
        t = dict(side=-1, minute=580, entry=100., stop=101., exit=99., exit_minute=900)
        (_, net, fee, _, _), = I.settle([("A", t, 100)])
        self.assertAlmostEqual(net, 100 - fee)
        self.assertGreater(fee, 2.)  # a 1 USD minimum commission per side


def daily(rows):
    """{symbol: {date: (raw o, raw c, vol, adj o, adj c)}} from (date, open, close) with adjusted == raw."""
    return {"X": {d: (o, c, 1000, o, c) for d, o, c in rows}}


class OvernightTests(unittest.TestCase):
    D = [date(2024, 1, 2), date(2024, 1, 3), date(2024, 1, 4)]

    def test_return_is_official_close_to_next_official_open(self):
        data = daily([(self.D[0], 100, 101), (self.D[1], 102, 103), (self.D[2], 99, 98)])
        legs = I.overnight_legs(data, lambda d: ["X"], self.D)
        self.assertEqual(legs[self.D[1]], [("X", 101, 102 / 101)])
        self.assertEqual(legs[self.D[2]], [("X", 103, 99 / 103)])
        self.assertNotIn(self.D[0], legs)

    def test_overnight_times_intraday_is_close_to_close(self):
        data = daily([(self.D[0], 100, 101), (self.D[1], 102, 103), (self.D[2], 99, 98)])
        night = I.overnight_legs(data, lambda d: ["X"], self.D)
        mirror = I.intraday_legs(data, lambda d: ["X"], self.D)
        for day, (close, previous) in zip(self.D[1:], [(103, 101), (98, 103)]):
            self.assertAlmostEqual(night[day][0][2] * mirror[day][0][2], close / previous)

    def test_dividend_adjusted_ratio_is_used(self):
        data = {"X": {self.D[0]: (100, 100, 1, 99, 99), self.D[1]: (98, 98, 1, 98, 98)}}
        self.assertAlmostEqual(I.overnight_legs(data, lambda d: ["X"], self.D[:2])[self.D[1]][0][2], 98 / 99)

    def test_half_day_session_uses_its_own_official_close(self):
        half = [date(2023, 11, 24), date(2023, 11, 27)]  # the day after Thanksgiving closes at 13:00
        data = daily([(half[0], 100, 100.5), (half[1], 101, 102)])
        self.assertEqual(I.overnight_legs(data, lambda d: ["X"], half)[half[1]], [("X", 100.5, 101 / 100.5)])

    def test_costs_and_slippage_reduce_the_result(self):
        legs = {self.D[1]: [("X", 100., 1.01)]}
        gross = I.run_legs(legs, self.D, 0, 10000.)[0][-1][1]
        slipped = I.run_legs(legs, self.D, 5, 10000.)[0][-1][1]
        self.assertGreater(gross, slipped)
        self.assertLess(gross, 10100.)  # 100 shares gain 100 USD before about 2 USD of fees
        self.assertGreater(gross, 10095.)


class UniverseTests(unittest.TestCase):
    def test_top_n_by_prior_month_dollar_volume_only(self):
        days = [date(2024, 1, d) for d in (2, 3, 4)] + [date(2024, 2, 1)]
        big = {d: (1, 10, 1000, 1, 10) for d in days[:3]} | {days[3]: (1, 10, 1, 1, 10)}
        small = {d: (1, 10, 10, 1, 10) for d in days[:3]} | {days[3]: (1, 10, 10 ** 9, 1, 10)}  # February surge unseen
        data = {"BIG": big, "SMALL": small, "NEW": {days[3]: (1, 10, 10 ** 9, 1, 10)}}
        self.assertEqual(I.monthly_universe(data, [(2024, 2)], n=1), {(2024, 2): ["BIG"]})
        self.assertEqual(I.monthly_universe(data, [(2024, 2)], n=5), {(2024, 2): ["BIG", "SMALL"]})

    def test_digest_mismatch_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "c.json")
            self.assertEqual(I._cached(path, lambda: ([1], 1)), [1])
            path.write_text(path.read_text().replace("[1]", "[2]", 1))
            with self.assertRaises(ValueError):
                I._cached(path, lambda: ([1], 1))


class MetricsTests(unittest.TestCase):
    def test_metrics_and_yearly(self):
        curve = [(date(2023, 12, 29), 100000.), (date(2024, 1, 2), 110000.), (date(2024, 1, 3), 99000.)]
        m = I.metrics(curve, [(curve[1][0], 10., 0.01)], 5., 100000.)
        self.assertAlmostEqual(m["max_drawdown"], -0.1)
        self.assertAlmostEqual(m["total_return"], -0.01)
        y = I.yearly(curve)
        self.assertEqual(sorted(y), [2023, 2024])
        self.assertAlmostEqual(y[2024], -0.01)

    def test_flat_curve_sharpe_is_none(self):
        curve = [(date(2024, 1, 2), 100000.), (date(2024, 1, 3), 100000.)]
        self.assertIsNone(I.metrics(curve)["sharpe"])


class StandardReportTests(unittest.TestCase):
    D = [date(2024, 1, 2), date(2024, 1, 3), date(2024, 1, 4), date(2024, 1, 5)]

    def test_leg_fills_feed_the_standard_report(self):
        legs = {self.D[2]: [("X", 100., 1.02)]}
        curve, trades, _ = I.run_legs(legs, self.D, 2, 10000.)
        fills = I.leg_fills(trades, "buy at open", "sell at close")
        n = trades[0][4]
        self.assertEqual([(f["side"], f["position_after"]) for f in fills], [("buy", n), ("sell", 0)])
        self.assertAlmostEqual(sum(f["fee"] for f in fills), trades[0][7])
        # P&L recomputed from the fill prices and fees matches the booked trade P&L.
        self.assertAlmostEqual((fills[1]["price"] - fills[0]["price"]) * n - trades[0][7], trades[0][1])
        spy = [(d, 10000. * (1 + 0.01 * i)) for i, d in enumerate(self.D)]
        with tempfile.TemporaryDirectory() as tmp:
            I.write_standard_report(Path(tmp, "r"), Path(tmp, "mc.json"), "t", curve, spy, fills, 10000., paths=20)
            text = Path(tmp, "r", "REPORT.md").read_text(encoding="utf-8")
            self.assertIn("p95", text)
            self.assertIn("| X | buy |", Path(tmp, "r", "trades_best_day.md").read_text(encoding="utf-8"))
            with self.assertRaises(ValueError):  # no fills at all
                I.write_standard_report(Path(tmp, "e"), Path(tmp, "e.json"), "t", curve, spy, [], 10000., paths=20)

    def test_orb_fills_mark_stops_and_signed_positions(self):
        t = dict(side=-1, minute=575., entry=50., stop=51., exit=51., exit_minute=600)
        fills = I.orb_fills([(self.D[0], "Y", t, 5000., 2., -102.)])
        self.assertEqual([(f["side"], f["quantity"], f["position_after"]) for f in fills], [("sell", 100, -100), ("buy", 100, 0)])
        self.assertIn("stop", fills[1]["reason"])
        self.assertAlmostEqual(sum(f["fee"] for f in fills), 2.)


if __name__ == "__main__":
    unittest.main()

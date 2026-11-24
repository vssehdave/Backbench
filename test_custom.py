"""Offline tests for strategies/custom/* on hand-made data."""
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

import customlib
import xsection

for name in ("faa", "momentum-60d", "sp500-top-holding", "munger-200wma"):
    sys.path.append(str(Path(__file__).parent / "strategies" / "custom" / name))
import faa_rules
import leader_rules
import mom60_rules
import munger_rules


def sessions(n, start=date(2016, 1, 4)):
    out, d = [], start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


class Seen:
    def __init__(self, dates, prices):
        self.dates, self.prices, self.date = tuple(dates), {s: tuple(p) for s, p in prices.items()}, dates[-1]


class FAA(unittest.TestCase):
    def series(self, growth, wobble=0.):
        return [100 * (1 + growth) ** t * (1 + wobble * (-1) ** t) for t in range(100)]

    def test_ranks_best_first_and_ties_by_order(self):
        self.assertEqual(faa_rules._ranks([3, 1, 2], True), [1, 3, 2])
        self.assertEqual(faa_rules._ranks([3, 1, 2], False), [3, 1, 2])
        self.assertEqual(faa_rules._ranks([1, 1, 1], True), [1, 2, 3])

    def test_top_three_by_momentum_equal_weight(self):
        growth = dict(VTI=.003, EFA=.002, EEM=.001, SHY=-.001, AGG=-.002, DBC=-.003, VNQ=-.004)
        seen = Seen(sessions(100), {s: self.series(g, .001 * (i + 1)) for i, (s, g) in enumerate(growth.items())})
        w = faa_rules.decide(seen)
        self.assertEqual(set(w), {"VTI", "EFA", "EEM"})
        self.assertAlmostEqual(sum(w.values()), 1.)

    def test_negative_momentum_pick_goes_to_cash(self):
        growth = dict(VTI=.003, EFA=-.002, EEM=-.002, SHY=-.0001, AGG=-.002, DBC=-.003, VNQ=-.004)
        seen = Seen(sessions(100), {s: self.series(g, .0005 * (i + 1)) for i, (s, g) in enumerate(growth.items())})
        w = faa_rules.decide(seen)
        self.assertAlmostEqual(w["VTI"], 1 / 3)
        self.assertAlmostEqual(w.get("SHY", 0), 2 / 3)  # two of the three slots fail the absolute test

    def test_abstains_without_four_months(self):
        self.assertIsNone(faa_rules.decide(Seen(sessions(50), {s: self.series(0)[:50] for s in faa_rules.UNIVERSE})))


class Momentum(unittest.TestCase):
    def test_signal_uses_close_sixty_sessions_back(self):
        history = [100.] * 10 + [50.] + [100.] * 59 + [120.]  # 71 closes; index -61 is the 50
        self.assertAlmostEqual(mom60_rules.signal(history), 120 / 50 - 1)
        history[-61] = 100.
        self.assertAlmostEqual(mom60_rules.signal(history), 0.2)

    def test_decide_long_cash_and_warmup(self):
        up, down = [100.] * 60 + [101.], [100.] * 60 + [99.]
        self.assertEqual((mom60_rules.decide(up, 60), mom60_rules.decide(down, 60)), (1, 0))
        self.assertEqual(mom60_rules.decide([100.] * 61, 60), 0)  # a zero signal is not positive
        self.assertIsNone(mom60_rules.decide(up[:60], 60))


class Leader(unittest.TestCase):
    def setUp(self):
        self.dates = sessions(30)
        self.adj = {"AAA": [10.] * 30, "BBB": [10.] * 30}
        self.raw = {"AAA": [10.] * 30, "BBB": [10.] * 30}
        self.members = {"AAA", "BBB"}

    def shares(self, bbb_rows):
        return {"AAA": (1, leader_rules.Shares([("2015-12-01", "2015-11-30", "a1", 100)])), "BBB": (2, leader_rules.Shares(bbb_rows))}

    def leader(self, i, shares):
        return leader_rules.leader(i, self.dates, self.adj, self.raw, shares, self.members)

    def test_filing_date_not_period_end_decides_visibility(self):
        late = self.shares([("2015-12-01", "2015-11-30", "b1", 50), (str(self.dates[20]), "2015-12-31", "b2", 200)])
        self.assertEqual(self.leader(19, late), "AAA")  # the 200 figure has a past period end but is not filed yet
        self.assertEqual(self.leader(20, late), "BBB")  # visible the day it is filed

    def test_future_filings_cannot_change_the_past(self):
        base = self.shares([("2015-12-01", "2015-11-30", "b1", 50)])
        later = self.shares([("2015-12-01", "2015-11-30", "b1", 50), (str(self.dates[25]), "2015-12-31", "b2", 9999)])
        self.assertEqual([self.leader(i, base) for i in range(25)], [self.leader(i, later) for i in range(25)])

    def test_split_after_period_end_does_not_distort_the_cap(self):
        # BBB splits 10:1 on session 10: raw falls to 1, adjusted is flat, the shares figure is pre-split.
        self.raw["BBB"] = [10.] * 10 + [1.] * 20
        self.adj["BBB"] = [1.] * 30
        shares = self.shares([("2015-12-01", "2015-11-30", "b1", 150)])  # 150 x 10 = 1500 > AAA's 1000
        self.assertEqual(self.leader(5, shares), "BBB")
        self.assertEqual(self.leader(20, shares), "BBB")

    def test_count_restated_for_a_later_split_is_priced_on_the_filing_day(self):
        # BBB splits 10:1 on session 10. On session 15 it files a post-split count (500) for an old period end.
        # Priced at the old period end (raw 10) it would be 5000 and falsely lead; on the filing day (raw 1) it is 500.
        self.raw["BBB"] = [10.] * 10 + [1.] * 20
        self.adj["BBB"] = [1.] * 30
        shares = self.shares([(str(self.dates[15]), "2015-12-31", "b1", 500)])
        self.assertEqual(self.leader(20, shares), "AAA")

    def test_stale_share_fact_is_ignored(self):
        old = leader_rules.Shares([("2015-12-01", "2015-11-30", "x", 100)])
        self.assertIsNotNone(old.at("2016-12-01"))
        self.assertIsNone(old.at("2017-02-01"))

    def test_share_classes_summed_and_counted_once_per_company(self):
        both = leader_rules.Shares([("2015-12-01", "2015-11-30", "x", 60), ("2015-12-01", "2015-11-30", "x", 70)])
        self.assertEqual(both.at("2016-01-01"), ("2015-12-01", 130))
        shares = {"AAA": (1, leader_rules.Shares([("2015-12-01", "2015-11-30", "a", 100)])), "BBB": (1, both)}
        caps = leader_rules.market_caps(5, self.dates, self.adj, self.raw, shares, self.members)
        self.assertEqual(list(caps), ["AAA"])

    def test_thousandfold_unit_slip_is_dropped(self):
        rows = [("2016-0%d-01" % k, "2016-0%d-01" % k, "a%d" % k, v) for k, v in enumerate((100, 100_000, 100, 100), 1)]
        self.assertEqual(leader_rules.Shares(rows).at("2016-03-15"), ("2016-03-01", 100))

    def test_non_members_cannot_lead_and_decision_is_lagged_one_session(self):
        shares = self.shares([("2015-12-01", "2015-11-30", "b1", 500)])
        self.assertEqual(leader_rules.leader(5, self.dates, self.adj, self.raw, shares, {"AAA"}), "AAA")
        self.raw["AAA"] = self.adj["AAA"] = [10.] * 11 + [100.] * 19  # AAA overtakes BBB on session 11
        panel = type("P", (), dict(dates=self.dates, adj=self.adj, raw=self.raw, members=[self.members] * 30))
        decide = leader_rules.make_decide(panel, shares)
        view = lambda n: Seen(self.dates[:n], {s: self.adj[s][:n] for s in self.adj})
        self.assertEqual(decide(view(12), None), {"BBB": 1.0})  # session 11 is the latest; the decision sees session 10
        self.assertEqual(decide(view(13), None), {"AAA": 1.0})


def rec(ni=(10, 11, 12, 13, 14), equity=50., debt=20.):
    """Five fiscal years 2019-2023 filed the following February (net income, equity, long-term debt)."""
    years = range(2019, 2024)
    return dict(ni=[[f"{y + 1}-02-15", f"{y}-01-01", f"{y}-12-31", v] for y, v in zip(years, ni)], ni2=[],
                eq=[[f"{y + 1}-02-15", f"{y}-12-31", equity] for y in years], eq2=[],
                ltd=[[f"{y + 1}-02-15", f"{y}-12-31", debt] for y in years], ltd_nc=[], ltd_c=[], debt_c=[], ltd_cap=[])


class Munger(unittest.TestCase):
    def setUp(self):
        self.dates = sessions(1010, date(2021, 1, 4))  # ends Oct 2024, after the FY2023 filings

    def test_weekly_ma_needs_200_weeks_and_uses_weekly_closes(self):
        self.assertIsNone(munger_rules.weekly_ma(self.dates[:995], [1.] * 995))
        # Monday-Thursday at 0, Friday at the week's number: only Fridays count.
        prices = [float(d.isocalendar()[1]) if d.weekday() == 4 else 0. for d in self.dates[:1000]]
        weeks = [p for p in prices if p]
        self.assertAlmostEqual(munger_rules.weekly_ma(self.dates[:1000], prices), sum(weeks[-200:]) / 200)

    def test_high_quality_screen_uses_only_filed_data(self):
        day = date(2024, 6, 1)
        self.assertTrue(munger_rules.high_quality(rec(), day))
        self.assertFalse(munger_rules.high_quality(rec(ni=(10, 11, -1, 13, 14)), day))  # a loss year
        self.assertFalse(munger_rules.high_quality(rec(debt=60.), day))  # debt/equity above 1
        self.assertFalse(munger_rules.high_quality(rec(ni=(2, 2, 2, 2, 2)), day))  # ROE 4%
        self.assertFalse(munger_rules.high_quality(rec(), date(2024, 1, 1)))  # FY2023 is filed only in Feb 2024

    def test_buy_at_or_below_ma_hold_until_x_above_and_state_persists(self):
        n = len(self.dates)
        records = {"GOOD": rec(), "BAD": rec(debt=60.)}

        def run(path, decide):
            return decide(Seen(self.dates[:len(path)], {"GOOD": path, "BAD": path, "NOREC": path}), None)

        flat = [100.] * n
        decide = munger_rules.make_decide(records, exit_above=.2)
        self.assertEqual(run(flat, decide), {"GOOD": 1.0})  # price equals the MA: at or below; BAD and NOREC fail quality
        self.assertEqual(run(flat[:-1] + [110.], decide), {"GOOD": 1.0})  # above the MA but under +20%: still held
        self.assertEqual(run(flat[:-1] + [125.], decide), {})  # 25% above the MA: sold
        self.assertEqual(run(flat[:-1] + [110.], decide), {})  # not re-bought while above the MA
        self.assertEqual(run(flat[:-1] + [110.], munger_rules.make_decide(records)), {})  # fresh state, never bought


class Metrics(unittest.TestCase):
    def test_cagr_from_calendar_days_and_daily_cadence(self):
        m = customlib.metrics([date(2020, 1, 1), date(2021, 1, 1)], [1., 1.1])
        self.assertAlmostEqual(m["cagr"], 1.1 ** (365.25 / 366) - 1, places=3)
        self.assertEqual(xsection.decision_indexes(list(range(10)), 2, 6, "daily"), [2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()

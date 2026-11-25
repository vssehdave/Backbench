"""Offline tests for the top-50 ORB study: point-in-time universe, range length, notional cap, features, statistics."""
import random
import unittest
from datetime import date, timedelta

import intraday as I
import orb_analysis as A
import orb_universe as U

leader_rules = U.leader_rules


def weekdays(start, n):
    out, d = [], start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def bars(spec, start=570):
    return [(start + i, *x) for i, x in enumerate(spec)]


class Universe(unittest.TestCase):
    def setUp(self):
        self.dates = weekdays(date(2016, 1, 4), 90)  # the last session of January 2016 is index 19
        flat = [10.] * 90
        names = ("AAA", "BBB", "CCC", "DDD")
        self.panel = type("P", (), dict(dates=self.dates, adj={s: flat for s in names}, raw={s: flat for s in names},
                                        members=[{"AAA", "BBB", "CCC"}] * 90))  # DDD is not a member
        self.old = ("2015-12-01", "2015-11-30")

    def shares(self, bbb):
        fact = lambda n: leader_rules.Shares([(*self.old, "a", n)])
        return {"AAA": (1, fact(100)), "BBB": (2, bbb), "CCC": (3, fact(50)), "DDD": (4, fact(10_000))}

    def top(self, shares, n=2):
        return U.top_by_cap(self.panel, shares, [(2016, 2)], n)[(2016, 2)]

    def test_top_n_by_cap_among_members_only(self):
        picks = self.top(self.shares(leader_rules.Shares([(*self.old, "b", 70)])))
        self.assertEqual(picks, [("AAA", 1000.), ("BBB", 700.)])

    def test_filing_on_or_after_the_ranking_day_is_not_used(self):
        ranking = U.ranking_index(self.dates, 2016, 2)
        for filed in (self.dates[ranking], self.dates[ranking + 1]):
            late = leader_rules.Shares([(*self.old, "b", 70), (str(filed), "2015-12-31", "b2", 900)])
            self.assertEqual(self.top(self.shares(late)), [("AAA", 1000.), ("BBB", 700.)])
        before = leader_rules.Shares([(*self.old, "b", 70), (str(self.dates[ranking - 1]), "2015-12-31", "b2", 900)])
        self.assertEqual(self.top(self.shares(before))[0], ("BBB", 9000.))

    def test_ranking_uses_the_last_session_before_the_month(self):
        i = U.ranking_index(self.dates, 2016, 2)
        self.assertEqual(self.dates[i], date(2016, 1, 29))
        self.assertIsNone(U.ranking_index(self.dates, 2016, 1))

    def test_company_without_facts_is_absent_not_an_error(self):
        shares = self.shares(leader_rules.Shares([]))
        del shares["BBB"]
        self.assertEqual([s for s, _ in self.top(shares, 5)], ["AAA", "CCC"])


class RangeLength(unittest.TestCase):
    # 09:30 to 09:39 range is 99 to 101; 09:40 to 09:44 widens it to 98 to 102.
    TEN = [(100, 101, 99, 100)] * 10
    FIFTEEN = TEN + [(100, 102, 98, 100)] * 5
    BREAK = [(101.5, 103, 101.4, 102.5), (102.6, 103, 102.5, 102.8)] + [(102.8, 103, 102.7, 102.8)] * 40

    def test_range_covers_exactly_n_bars(self):
        b = bars(self.FIFTEEN)
        self.assertEqual(I.opening_range(b, 5), (101, 99))
        self.assertEqual(I.opening_range(b, 10), (101, 99))
        self.assertEqual(I.opening_range(b, 15), (102, 98))
        self.assertIsNone(I.opening_range(b[:9], 10))

    def test_no_trigger_inside_the_range_window(self):
        # The 09:36 close is above 101: a signal for the 5-minute range, inside the window of the 10-minute one.
        spec = [(100, 101, 99, 100)] * 6 + [(100, 102, 100, 101.5), (101.5, 102, 101.4, 101.6)] + [(101.6, 102, 101.5, 101.6)] * 40
        self.assertIsNotNone(I.orb_day(bars(spec), 960, 0, True, 5))
        self.assertIsNone(I.orb_day(bars(spec), 960, 0, True, 10))

    def test_first_trigger_bar_and_stop_follow_the_range(self):
        for minutes, stop, trigger in ((10, 99, 10), (15, 102 - 4, 15)):
            spec = (self.TEN if minutes == 10 else self.FIFTEEN) + self.BREAK
            t = I.orb_day(bars(spec), 960, 0, True, minutes)
            self.assertEqual((t["side"], t["stop"], t["minute"]), (1, stop, 570 + trigger + 1))


class NotionalCap(unittest.TestCase):
    def test_cap_binds_on_tight_ranges_and_is_off_by_default(self):
        t = dict(side=1, minute=580, entry=100., stop=99.99, exit=100., exit_minute=900)
        (_, _, free), = I.size_trades([("A", t)], 100000., 0.01, 4.)
        (_, _, capped), = I.size_trades([("A", t)], 100000., 0.01, 4., max_positions=50)
        self.assertEqual((free, capped), (4000, 20))  # 100000 / 50 / 100

    def test_risk_size_is_kept_below_the_cap(self):
        t = dict(side=1, minute=580, entry=100., stop=90., exit=100., exit_minute=900)
        (_, _, shares), = I.size_trades([("A", t)], 100000., 0.01, 4., max_positions=5)
        self.assertEqual(shares, 100)  # 1000 risk over 10 per share; the cap would allow 200

    def test_all_positions_together_never_exceed_equity(self):
        trades = [(s, dict(side=1, minute=580 + i, entry=100.37, stop=100.36, exit=100., exit_minute=900))
                  for i, s in enumerate("ABCDEFGHIJ")]
        sized = I.size_trades(trades, 100000., 0.01, 4., max_positions=10)
        self.assertEqual(len(sized), 10)
        self.assertLessEqual(sum(n * t["entry"] for _, t, n in sized), 100000.)

    def test_gross_stays_within_equity_when_more_positions_open_than_the_divisor(self):
        trades = [(s, dict(side=1, minute=580 + i, entry=100.37, stop=100.36, exit=100., exit_minute=900))
                  for i, s in enumerate("ABCDEFGHIJ")]
        sized = I.size_trades(trades, 100000., 0.01, 4., max_positions=5)
        self.assertEqual([n for _, _, n in sized], [199] * 5 + [1])  # leverage 4 alone would have let all ten in
        self.assertLessEqual(sum(n * t["entry"] for _, t, n in sized), 100000.)


class Features(unittest.TestCase):
    def setUp(self):
        self.days = weekdays(date(2024, 1, 2), 80)
        self.daily = {d: (100 + i, 100 + i, 1000, 100 + i, 100 + i) for i, d in enumerate(self.days)}
        self.hl = {d: (101 + i, 99 + i, 100 + i) for i, d in enumerate(self.days)}
        self.spy = {d: (0, 0, 0, 0, 100 + (i * 7) % 5) for i, d in enumerate(self.days)}

    def history(self, wild_from=None):
        """The same history, but every bar from wild_from on is replaced with absurd values."""
        wild = lambda d: wild_from is not None and d >= wild_from
        return U.History({d: (1, 1, 10 ** 9, 1, 1) if wild(d) else v for d, v in self.daily.items()},
                         {d: (500, 1, 1) if wild(d) else v for d, v in self.hl.items()},
                         {d: (5, 5, 5, 5, 5) if wild(d) else v for d, v in self.spy.items()})

    def test_features_ignore_the_trade_day_and_later(self):
        day = self.days[70]
        a, b = self.history(), self.history(wild_from=day)
        for name in ("atr_pct", "dollar_volume", "prior_close", "beta"):
            self.assertEqual(getattr(a, name)(day), getattr(b, name)(day), name)

    def test_gap_uses_the_open_of_the_day_and_nothing_after_it(self):
        day = self.days[30]
        self.assertAlmostEqual(self.history().gap(day), 130 / 129 - 1)
        later = self.history(wild_from=self.days[31])
        self.assertEqual(later.gap(day), self.history().gap(day))

    def test_atr_is_mean_true_range_over_prior_20_sessions_over_prior_close(self):
        h = self.history()
        # high - low is 2 and each close steps up 1, so the true range is 2 every day.
        self.assertAlmostEqual(h.atr_pct(self.days[40]), 2 / self.hl[self.days[39]][2])
        self.assertIsNone(h.atr_pct(self.days[10]))

    def test_dollar_volume_is_the_prior_calendar_month(self):
        day = self.days[30]
        month = [d for d in self.days if (d.year, d.month) == (day.year, day.month - 1)]
        self.assertAlmostEqual(self.history().dollar_volume(day), sum(self.daily[d][1] * 1000 for d in month) / len(month))

    def test_beta_needs_history_and_recovers_a_known_slope(self):
        px_spy, px, level = {}, {}, [100., 100.]
        for i, d in enumerate(self.days):
            r = 0.01 * ((i * 7) % 5 - 2)
            level = [level[0] * (1 + r), level[1] * (1 + 2 * r)]
            px_spy[d], px[d] = (0, 0, 0, 0, level[0]), (0, 0, 0, 0, level[1])
        h = U.History(px, {}, px_spy)
        self.assertIsNone(h.beta(self.days[30]))
        self.assertAlmostEqual(h.beta(self.days[79]), 2, delta=0.1)


class Statistics(unittest.TestCase):
    def trades(self, rets, symbol="A", start=date(2020, 1, 1)):
        return [dict(day=start + timedelta(days=i), symbol=symbol, ret=r, pnl=r * 1000, f=dict(x=i)) for i, r in enumerate(rets)]

    def test_stock_stats(self):
        s = A.stock_stats(self.trades([0.01, -0.005, 0.01, 0.0]))["A"]
        self.assertEqual((s["n"], s["win_rate"]), (4, 0.5))
        self.assertAlmostEqual(s["profit_factor"], 4.0)
        self.assertAlmostEqual(s["mean_bps"], 37.5)

    def test_quintiles_pick_up_a_monotone_feature(self):
        q = A.quintiles(self.trades([i / 1000 for i in range(100)]), "x")
        self.assertAlmostEqual(q["rho"], 1.0)
        self.assertGreater(q["top_minus_bottom_bps"], 0)
        self.assertEqual(A.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)

    def test_winners_vs_rest_splits_by_total_pnl_and_compares_stock_means(self):
        trades = []
        for k in range(10):  # stock k earns k bps per trade and has feature x = k
            trades += [dict(day=date(2020, 1, 1), symbol=f"S{k}", ret=k / 1e4, pnl=k, f=dict(x=k, sector="A" if k < 5 else "B"))
                       for _ in range(5)]
        w = A.winners_vs_rest(trades, ["x"], top=0.2, min_trades=5)
        self.assertEqual((w["winners"], w["eligible"]), (["S9", "S8"], 10))
        self.assertEqual((w["features"]["x"]["winners_median"], w["features"]["x"]["rest_median"]), (8.5, 3.5))
        self.assertAlmostEqual(w["features"]["x"]["rho_with_pnl"], 1.0)
        self.assertEqual(w["sectors"], {"B": [2, 3], "A": [0, 5]})

    def test_rule_cut_points_come_from_the_first_half_only(self):
        first = self.trades([0.0] * 30, start=date(2020, 1, 1))  # x = 0..29, so the terciles cut at 10 and 20
        second = self.trades([0.01] * 30, start=date(2023, 1, 1))
        top = [r for r in A.feature_rules(first, second, ["x"]) if r["rule"] == "top"][0]
        self.assertEqual((top["first_half_n"], top["second_half_n"]), (10, 10))
        self.assertAlmostEqual(top["second_half_bps"], 100.)

    def test_stocks_picked_on_noise_do_not_beat_the_rest_out_of_sample(self):
        rng = random.Random(3)
        first, second = [], []
        for k in range(30):
            first += self.trades([rng.gauss(0, 0.01) for _ in range(80)], f"S{k}", date(2020, 1, 1))
            second += self.trades([rng.gauss(0, 0.01) for _ in range(80)], f"S{k}", date(2023, 1, 1))
        p = A.persistence(first, second)
        self.assertEqual(len(p["picked"]), 6)
        self.assertGreater(p["picked_first_half_bps"], 10)
        self.assertLess(abs(p["picked_second_half_bps"]), 20)

    def test_shuffle_test_finds_few_lucky_stocks_in_pure_noise(self):
        rng = random.Random(5)
        trades = [dict(day=date(2020, 1, 1) + timedelta(days=i), symbol=f"S{k}", ret=rng.gauss(0, 0.01), pnl=0., f={})
                  for k in range(20) for i in range(120)]
        c = A.shuffle_test(trades, date(2020, 3, 1), sims=20, min_trades=50)
        self.assertEqual(c["stocks"], 20)
        self.assertLessEqual(c["chance_count_mean"], 3)


if __name__ == "__main__":
    unittest.main()

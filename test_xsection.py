import json
import math
import random
import unittest
from datetime import date, timedelta
from pathlib import Path

import xs_data
import xsection as xs
from xsection import Costs, Limits

ZERO = Costs(0, 0, 0, 0, 0, 0, 0)
LOOSE = Limits(max_gross=1.0, max_net=1.0, name_cap=1.0)


def sessions(first, n):
    out, day = [], first
    while len(out) < n:
        if day.weekday() < 5:
            out.append(day)
        day += timedelta(days=1)
    return out


def panel_of(dates, adj, raw=None, members=None):
    raw = raw or adj
    return xs_data.Panel(dates, adj, raw, members)


def walk(seed, n, start=100.):
    rng, p, out = random.Random(seed), start, []
    for _ in range(n):
        p *= math.exp(rng.gauss(0.0003, 0.01))
        out.append(p)
    return out


def momentum_pick(seen, params):
    """Reads prices: long the best 1 name and short the worst 1 name by return since the first bar."""
    score = {s: p[-1] / p[0] for s, p in seen.prices.items()}
    ranked = sorted(score, key=score.get)
    return {ranked[0]: -0.5, ranked[-1]: 0.5}


class Engine(unittest.TestCase):
    def setUp(self):
        self.dates = sessions(date(2024, 1, 2), 90)
        self.adj = {s: walk(i, 90) for i, s in enumerate("ABCDE")}

    def run_window(self, adj, decide, i1=80, limits=LOOSE, costs=ZERO, cadence="monthly", dates=None):
        panel = panel_of(dates or self.dates, adj)
        return xs.run_window(panel, decide, None, 5, i1, limits, costs, cadence, 100000.)

    def test_no_lookahead(self):
        base = self.run_window(self.adj, momentum_pick)
        cut = 45
        future = {s: p[:cut + 1] + [x * 3 for x in p[cut + 1:]] for s, p in self.adj.items()}
        changed = self.run_window(future, momentum_pick)
        before = [d for d in base["decisions"] if d[0] <= str(self.dates[cut])]
        self.assertTrue(before)
        self.assertEqual(before, [d for d in changed["decisions"] if d[0] <= str(self.dates[cut])])
        # The positive control: moving the price on the decision day itself must change the decision.
        decision_day = next(i for i, d in enumerate(self.dates) if str(d) == before[-1][0])
        poked = {s: p[:] for s, p in self.adj.items()}
        for s in poked:
            poked[s][decision_day] *= 5 if s == "A" else 1
        self.assertNotEqual(before[-1], self.run_window(poked, momentum_pick)["decisions"][len(before) - 1])

    def test_view_truncates_at_the_decision_date(self):
        seen = xs.view(panel_of(self.dates, self.adj), 30)
        self.assertEqual(seen.date, self.dates[30])
        self.assertEqual({len(p) for p in seen.prices.values()}, {31})
        self.assertEqual(len(seen.dates), 31)

    def test_buy_costs_use_raw_price_for_shares(self):
        dates = sessions(date(2024, 1, 2), 8)
        run = xs.run_window(panel_of(dates, {"A": [50.] * 8}, {"A": [100.] * 8}), lambda s, p: {"A": 0.5}, None,
                            2, 6, LOOSE, Costs(), "monthly", 100000.)
        # 50,000 USD at a raw 100 is 500 shares: 500 * 0.0035 = 1.75 commission; buys carry only 500 * 0.000003.
        self.assertAlmostEqual(run["costs"]["commission"], 1.75)
        self.assertAlmostEqual(run["costs"]["regulatory"], 0.0015)
        self.assertAlmostEqual(run["costs"]["slippage"], 25.0)
        self.assertAlmostEqual(run["equity"][-1], 100000 - 1.75 - 0.0015 - 25.0)
        self.assertAlmostEqual(run["traded"], 50000.)

    def test_commission_minimum_and_one_percent_cap(self):
        costs = Costs()
        self.assertEqual(xs.trade_costs(1000, 100, costs)[0], 0.35)  # 10 shares: 0.035 -> minimum 0.35
        self.assertAlmostEqual(xs.trade_costs(10, 100, costs)[0], 0.10)  # capped at 1% of 10 USD

    def test_short_borrow_fee_accrues_per_calendar_day(self):
        dates = [date(2024, 1, 4), date(2024, 1, 5), date(2024, 1, 8), date(2024, 1, 9)]  # Thu Fri Mon Tue
        run = xs.run_window(panel_of(dates, {"A": [50.] * 4}), lambda s, p: {"A": -0.5}, None, 0, 3, LOOSE,
                            Costs(commission_min=0, commission_per_share=0, slippage_bps=0), "monthly", 100000.)
        # Short 50,000 USD entered on Friday's close. Monday owes 3 days and Tuesday 1 day at 50 bps a year.
        expected = 50000 * 0.005 * (3 + 1) / 365
        self.assertAlmostEqual(run["costs"]["borrow"], expected)
        sell_fee = 50000 * 0.0000206 + 1000 * 0.000003
        self.assertAlmostEqual(run["equity"][-1], 100000 - expected - sell_fee)
        self.assertAlmostEqual(run["short_pnl"], 0.)

    def test_leverage_doubles_exposure_and_charges_margin_on_negative_cash(self):
        dates = [date(2024, 1, 4), date(2024, 1, 5), date(2024, 1, 8), date(2024, 1, 9)]  # Thu Fri Mon Tue
        costs = Costs(commission_min=0, commission_per_share=0, slippage_bps=0, sell_fee_per_share=0, margin_bps=300)
        run = xs.run_window(panel_of(dates, {"A": [50.] * 4}), lambda s, p: {"A": 2.}, None, 0, 3,
                            Limits(2., 2., 2.), costs, "monthly", 100000.)
        self.assertAlmostEqual(run["units"]["A"] * 50, 200000.)  # 2x equity, half of it borrowed
        monday = 100000 * 0.03 * 3 / 365
        tuesday = (100000 + monday) * 0.03 / 365
        self.assertAlmostEqual(run["costs"]["borrow"], monday + tuesday)
        self.assertAlmostEqual(run["equity"][-1], 100000 - monday - tuesday)

    def test_leg_pnl_and_equity_reconcile(self):
        run = self.run_window(self.adj, momentum_pick)
        self.assertAlmostEqual(run["equity"][-1] - run["equity"][0], run["long_pnl"] + run["short_pnl"], places=6)

    def test_weight_limits(self):
        limits = Limits(max_gross=1.0, max_net=0.0, name_cap=0.05)
        w = xs.enforce({"A": 0.9, "B": -0.9, "C": 0.02}, limits)
        self.assertLessEqual(max(abs(x) for x in w.values()), 0.05)
        self.assertAlmostEqual(sum(w.values()), 0.0)
        gross = xs.enforce({"A": 1.5, "B": -1.5}, Limits(1.0, 1.0, 5.0))
        self.assertAlmostEqual(sum(abs(x) for x in gross.values()), 1.0)
        self.assertEqual(xs.enforce({"A": 1.0}, Limits(1.0, 0.0, 1.0)), {})  # long-only cannot be net-flat
        with self.assertRaises(ValueError):
            xs.enforce({"A": float("nan")}, limits)

    def test_engine_applies_limits_and_rejects_unknown_symbols(self):
        run = self.run_window(self.adj, lambda s, p: {"A": 1.0, "B": -1.0}, limits=Limits(1.0, 0.0, 0.1))
        self.assertTrue(all(abs(x) <= 0.1 for _, w in run["decisions"] for x in w.values()))
        with self.assertRaises(ValueError):
            self.run_window(self.adj, lambda s, p: {"ZZZ": 0.1})

    def test_delisted_symbol_is_closed_at_its_last_price(self):
        dates = sessions(date(2024, 1, 2), 12)
        b = [20.] * 6 + [22., 25.] + [None] * 4
        panel = panel_of(dates, {"A": [10.] * 12, "B": b})
        run = xs.run_window(panel, lambda s, p: {"B": 0.5}, None, 1, 11, LOOSE, ZERO, "monthly", 1000.)
        # Bought 500 USD of B at 20, last bar 25, then gone: 500 + 500 * 25 / 20.
        self.assertEqual(run["forced_closes"], 1)
        self.assertEqual(run["units"], {})
        self.assertAlmostEqual(run["cash"], 500 + 625)
        self.assertAlmostEqual(run["equity"][-1], 1125.)

    def test_one_day_gap_carries_the_last_price(self):
        dates = sessions(date(2024, 1, 2), 8)
        panel = panel_of(dates, {"B": [20., 20., 20., None, 24., 24., 24., 24.]})
        run = xs.run_window(panel, lambda s, p: {"B": 0.5}, None, 1, 7, LOOSE, ZERO, "monthly", 1000.)
        self.assertEqual(run["forced_closes"], 0)
        self.assertAlmostEqual(run["equity"][-1], 500 + 500 * 24 / 20)

    def test_membership_gates_the_universe(self):
        panel = panel_of(self.dates, self.adj, members=[frozenset("AB")] * 90)
        self.assertEqual(set(xs.view(panel, 40).prices), {"A", "B"})

    def test_schedule(self):
        dates = sessions(date(2024, 1, 29), 12)  # Mon 29 Jan .. Tue 13 Feb
        i = xs.decision_indexes(dates, 0, 11, "monthly")
        self.assertEqual([str(dates[x]) for x in i], ["2024-01-29", "2024-01-31"])
        w = xs.decision_indexes(dates, 0, 11, "weekly")
        self.assertEqual([str(dates[x]) for x in w], ["2024-01-29", "2024-02-02", "2024-02-09"])
        schedule = list(xs.folds(date(2016, 1, 1), date(2026, 11, 1)))
        self.assertEqual(len(schedule), 10)
        self.assertEqual(schedule[0], (date(2016, 1, 1), date(2016, 7, 1), date(2017, 1, 1)))
        self.assertEqual(schedule[-1][2], date(2026, 1, 1))


class Study(unittest.TestCase):
    def setUp(self):
        self.dates = sessions(date(2023, 10, 2), 400)
        self.adj = {s: walk(i, 400) for i, s in enumerate(["SPY", "A", "B", "C", "D"])}
        self.panel = panel_of(self.dates, self.adj)
        self.levels = [dict(), dict(flip=True)]

    def go(self, fit=None):
        def decide(seen, params):
            w = momentum_pick(seen, params)
            return {s: -x for s, x in w.items()} if params.get("flip") else w
        return xs.study(self.panel, (decide, fit), self.levels, LOOSE, Costs(), "monthly", date(2024, 1, 1),
                        date(2025, 1, 1))

    def test_rerun_is_deterministic(self):
        first, second = self.go(), self.go()
        self.assertEqual(json.dumps(first, default=str), json.dumps(second, default=str))
        self.assertEqual(len(first), 1)
        self.assertEqual(first[0]["test_start"], "2024-07-01")
        self.assertEqual(first[0]["benchmarks"]["cash"]["total_return"], 0.0)
        self.assertEqual(len(first[0]["equity"]), len(first[0]["bench_equity"]["spy"]))

    def test_fit_sees_only_data_before_the_window(self):
        seen = []

        def fit(view, level):
            seen.append(view.date)
            return level

        self.go(fit)
        self.assertEqual(seen[-1], date(2024, 6, 28))  # the last session before the test window
        self.assertTrue(all(d < date(2024, 7, 1) for d in seen))


class Strategies(unittest.TestCase):
    folder = Path(__file__).parent / "strategies" / "xs"

    def setUp(self):
        import sys
        if str(self.folder) not in sys.path:
            sys.path.insert(0, str(self.folder))

    def test_manifests_load(self):
        for name in ("momentum_12_1", "low_volatility"):
            manifest, (decide, fit) = xs.load_manifest(self.folder / f"{name}.json")
            self.assertTrue(callable(decide))

    def test_bad_manifest_lists_every_problem(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "m.json"
            path.write_text(json.dumps(dict(id="x y", cadence="daily", entry="nope:fn", levels=[], extra=1)))
            with self.assertRaises(ValueError) as caught:
                xs.load_manifest(path)
        for text in ("missing field: limits", "unknown field: extra", "cadence", "id may only", "levels", "nope"):
            self.assertIn(text, str(caught.exception))

    def test_momentum_is_dollar_neutral_and_picks_the_extremes(self):
        import momentum_12_1  # on sys.path through load_manifest
        prices = {f"S{i}": tuple(100 * (1 + i / 100) ** (k / 25) for k in range(300)) for i in range(20)}
        # The last 21 bars are skipped, so a late spike must not matter.
        prices["S0"] = prices["S0"][:-21] + (1e6,) * 21
        w = momentum_12_1.decide(xs.AsOf(date(2024, 1, 1), (), prices), dict(lookback=252, skip=21, share=0.1))
        self.assertAlmostEqual(sum(w.values()), 0.0)
        self.assertEqual(sorted(w), ["S0", "S1", "S18", "S19"])
        self.assertIsNone(momentum_12_1.decide(xs.AsOf(date(2024, 1, 1), (), {"A": (1.,) * 10}),
                                               dict(lookback=252, skip=21, share=0.1)))

    def test_low_volatility_takes_the_calmest_names(self):
        import low_volatility
        prices = {f"S{i}": tuple(100 + (i + 1) * (-1) ** k for k in range(300)) for i in range(10)}
        w = low_volatility.decide(xs.AsOf(date(2024, 1, 1), (), prices), dict(window=252, share=0.2))
        self.assertEqual(sorted(w), ["S0", "S1"])
        self.assertAlmostEqual(sum(w.values()), 1.0)


class Universe(unittest.TestCase):
    def test_membership_undoes_later_changes(self):
        changes = [(date(2020, 3, 1), "B", "C", ""), (date(2019, 1, 1), "A", "D", "")]  # newest first
        dates = [date(2018, 6, 1), date(2019, 6, 1), date(2021, 1, 1)]
        sets, bad = xs_data.membership(["A", "B"], changes, dates)
        self.assertEqual(sets, [frozenset("CD"), frozenset("AC"), frozenset("AB")])
        self.assertEqual(bad, 0)

    def test_table_parser_skips_headers_and_reference_marks(self):
        html = ('<table id="changes"><tr><th>Date</th><th>Added</th></tr>'
                '<tr><td>June 1, 2020</td><td>ABC<sup>[1]</sup></td></tr></table><table id="other"><tr><td>x</td></tr></table>')
        parser = xs_data._Rows("changes")
        parser.feed(html)
        self.assertEqual(parser.rows, [["June 1, 2020", "ABC"]])

    def test_coverage_counts_missing_and_truncated_histories(self):
        dates = sessions(date(2024, 1, 2), 30)
        adj = {"A": [1.] * 30, "B": [1.] * 10 + [None] * 20}
        members = [frozenset("ABC")] * 30
        report = xs_data.coverage(panel_of(dates, adj, members=members), 0, 29, tolerance=2)
        self.assertEqual(report["members_without_any_data"], 1)
        self.assertEqual(report["missing_symbols"], ["C"])
        self.assertEqual(report["early_symbols"], ["B"])
        self.assertTrue(report["survivorship_biased"])
        self.assertAlmostEqual(report["member_day_coverage"], (30 + 10) / 90)


if __name__ == "__main__":
    unittest.main()

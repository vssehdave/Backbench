import unittest
from datetime import date
from controls import MeanThreshold, cash, threshold
from harness import fees, fixture, replay, study, trend_attribution


class ResearchChecks(unittest.TestCase):
    def test_regime_known_at_open_reconciles_to_total(self):
        train = [(None, 0, price) for price in range(80, 101)]
        forward = [(None, 0, 50), (None, 0, 200)]
        groups = trend_attribution(train, forward, [9900, 9970], 10000)
        self.assertEqual(groups["rising"], {"sessions": 1, "net_pnl_usd": -100})
        self.assertEqual(groups["falling"], {"sessions": 1, "net_pnl_usd": 70})
        self.assertEqual(sum(g["net_pnl_usd"] for g in groups.values()), -30)

    def test_fitted_strategy_uses_only_pre_cutoff_rows(self):
        fits = []
        class Logged(MeanThreshold):
            @staticmethod
            def fit(rows, offset):
                fits.append((rows[0][0], rows[-1][0], offset))
                return MeanThreshold.fit(rows, offset)
        def evaluate(rows):
            return study(rows, Logged, [-1, 0, 1], 3, 5, 42,
                         date(2022, 7, 1), date(2023, 1, 1))[0]
        rows = fixture()
        baseline = evaluate(rows)
        self.assertEqual(len(fits), 4)  # one selection fit on the first quarter, three artifacts on the warm-up
        self.assertEqual([last.month for _, last, _ in fits], [3] + [6]*3)
        self.assertTrue(all(first == date(2022,1,3) for first, _, _ in fits))
        self.assertGreater(min(baseline["forward_buys"], baseline["forward_sells"]), 0)
        cut = date(2022,9,1)
        changed = [(d, o*2 if d > cut else o, c*2 if d >= cut else c) for d,o,c in rows]
        other = evaluate(changed)
        self.assertEqual(baseline["train_scores"], other["train_scores"])
        self.assertEqual(baseline["selected"], other["selected"])
        prior = lambda fold: [t for t in fold["fills"] if t["date"] <= cut.isoformat()]
        self.assertEqual(prior(baseline), prior(other))

    def test_published_commission_examples_and_sell_fee(self):
        for qty, price, expected in [(100,25,1), (1000,25,5), (1000,.25,2.5)]:
            self.assertEqual(fees(qty, price)[0], expected)
        self.assertGreater(fees(-10, 100)[1], fees(10, 100)[1])

    def test_hand_accounted_round_trip(self):
        rows = [(date(2023,1,3),100,90), (date(2023,1,4),95,95)]
        state, _, trades = replay(rows, threshold, 99, (10000,0), [101])
        self.assertEqual([t["shares"] for t in trades], [10,-10])
        self.assertAlmostEqual(state[0], 10000-50-2-20*.000003-950*.0000206)

    def test_perturbation_changes_decision(self):
        rows = [(date(2023,1,d),100,100) for d in range(1,8)]
        def run(shock):
            return replay(rows,threshold,100,(10000,0),[100],42,shock)
        self.assertEqual(run(0)[2], [])
        self.assertTrue(run(100)[2])
        self.assertEqual(run(100), run(100))

    def test_future_prices_cannot_change_prior_orders(self):
        rows = fixture()
        def first_batch(bars):
            return study(bars, threshold, [98,100,102], 1, 0, 42,
                         date(2022, 7, 1), date(2023, 1, 1))[0]
        baseline = first_batch(rows)
        for i, (day, opening, close) in enumerate(rows):
            if not date(2022,7,1) <= day < date(2023,1,1):
                continue
            # At today's open even today's close is unknown.
            altered = rows[:i] + [(day, opening, close * 2)]
            altered.extend((d, o * 2, c * 2) for d,o,c in rows[i+1:])
            replayed = first_batch(altered)
            self.assertEqual(baseline["selected"], replayed["selected"])
            def through_open(fold):
                return [t for t in fold["fills"] if t["date"] <= day.isoformat()]
            self.assertEqual(through_open(baseline), through_open(replayed))

    WF = {"train_months": 6, "test_months": 6}

    def test_continuous_run_covers_every_session_from_one_level(self):
        rows = fixture()
        folds = study(rows, threshold, [98, 100, 102], 2, 0, 42, date(2022, 7, 1), date(2024, 1, 1))
        self.assertEqual(len(folds), 1)
        self.assertEqual(folds[0]["dates"], [str(r[0]) for r in rows if date(2022, 7, 1) <= r[0] < date(2024, 1, 1)])
        self.assertEqual(folds[0]["selected"], 98)

    def test_walk_forward_windows_tile_the_period_and_train_before_test(self):
        rows = fixture()
        folds = study(rows, threshold, [98, 100, 102], 2, 0, 42, date(2022, 7, 1), date(2024, 1, 1),
                      walk_forward=self.WF)
        self.assertEqual([(f["forward_start"], f["end_exclusive"]) for f in folds],
                         [("2022-07-01", "2023-01-01"), ("2023-01-01", "2023-07-01"), ("2023-07-01", "2024-01-01")])
        self.assertEqual([d for f in folds for d in f["dates"]],
                         [str(r[0]) for r in rows if date(2022, 7, 1) <= r[0] < date(2024, 1, 1)])
        for f in folds:
            self.assertLess(f["selection_start"], f["forward_start"])

    def test_folds_and_future_isolation(self):
        rows = fixture()
        def evaluate(data, strategy):
            return study(data,strategy,[98,100,102],2,0,42,date(2022,7,1),date(2024,1,1), walk_forward=self.WF)
        folds = evaluate(rows,threshold)
        self.assertEqual([(f["train_start"], f["forward_start"], f["end_exclusive"])
                          for f in folds], [
            ("2022-01-03", "2022-07-01", "2023-01-01"),
            ("2022-07-01", "2023-01-01", "2023-07-01"),
            ("2023-01-02", "2023-07-01", "2024-01-01")])
        for fold in folds:
            lo, hi = date.fromisoformat(fold["train_start"]), date.fromisoformat(fold["forward_start"])
            train = [r for r in rows if lo <= r[0] < hi]
            forward = [r for r in rows if str(r[0]) in fold["dates"]]
            _, expected, orders = replay(forward, threshold, fold["selected"],
                                         (10000., 0), [r[2] for r in train])
            self.assertEqual((fold["equity"], fold["fills"]), (expected, orders))
            self.assertGreater(fold["forward_buys"], 0)
            self.assertGreater(fold["forward_sells"], 0)
        altered = [(d,o*2 if d >= date(2023,7,1) else o,c*2 if d >= date(2023,7,1) else c) for d,o,c in rows]
        self.assertEqual(folds[:2], evaluate(altered, threshold)[:2])
        changed = [(d,o,c*2 if d >= date(2022,7,1) else c) for d,o,c in rows]
        self.assertEqual(folds[0]["train_scores"],evaluate(changed,threshold)[0]["train_scores"])
        for fold in evaluate(rows,cash):
            self.assertEqual(set(fold["equity"]), {10000})
        for fold in folds:
            self.assertEqual(fold["equity"][-1],fold["scenarios"][0]["ending_equity"])

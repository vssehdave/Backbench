import unittest
from datetime import date
from controls import cash, threshold
from harness import fees, fixture, replay, study


class ResearchChecks(unittest.TestCase):
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
                         date(2022,1,1), date(2023,1,1))[0]
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

    def test_folds_and_future_isolation(self):
        rows = fixture()
        def evaluate(data, strategy):
            return study(data,strategy,[98,100,102],2,0,42,date(2022,1,1),date(2024,1,1))
        folds = evaluate(rows,threshold)
        self.assertEqual([(f["train_start"], f["forward_start"], f["end_exclusive"])
                          for f in folds], [
            ("2022-01-01", "2022-07-01", "2023-01-01"),
            ("2023-01-01", "2023-07-01", "2024-01-01")])
        for year, fold in zip((2022, 2023), folds):
            train = [r for r in rows if r[0].year == year and r[0].month <= 6]
            forward = [r for r in rows if r[0].year == year and r[0].month > 6]
            _, expected, orders = replay(forward, threshold, fold["selected"],
                                         (10000., 0), [r[2] for r in train])
            self.assertEqual((fold["equity"], fold["fills"]), (expected, orders))
            self.assertGreater(fold["forward_buys"], 0)
            self.assertGreater(fold["forward_sells"], 0)
        altered = [(d,o,c*2 if d.year == 2022 and d.month > 6 else c) for d,o,c in rows]
        self.assertEqual(folds[1], evaluate(altered, threshold)[1])
        changed = [(d,o,c*2 if d >= date(2022,7,1) else c) for d,o,c in rows]
        self.assertEqual(folds[0]["train_scores"],evaluate(changed,threshold)[0]["train_scores"])
        for fold in evaluate(rows,cash):
            self.assertEqual(set(fold["equity"]), {10000})
        for fold in folds:
            self.assertEqual(fold["equity"][-1],fold["scenarios"][0]["ending_equity"])

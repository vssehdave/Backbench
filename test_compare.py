import copy
import unittest

from compare import compare


def example():
    return {
        "config": {"strategy": "a", "start": "2022-01-01", "end": "2023-01-01",
                   "paths": 2, "seed": 42, "shock_bps": 5, "symbol": "FIXTURE"},
        "source": "synthetic", "currency": "USD", "data_sha256": "fixture-hash",
        "execution_contract": {"engine_sha256": "revision", "fee_profile": "fixed",
                               "starting_cash": 100.},
        "folds": [{"train_start": "2022-01-01", "forward_start": "2022-07-01",
                   "end_exclusive": "2023-01-01", "equity": [90, 99], "selected": 1,
                   "forward_return": -.01, "selection_start": "2022-01-03",
                   "selection_return": .05, "fills": [{"commission": 1, "regulatory": .1}],
                   "scenarios": [{"seed": 42, "ending_equity": 101},
                                 {"seed": 43, "ending_equity": 95}]}],
    }


class CompareTests(unittest.TestCase):
    def test_drawdown_and_paths_aligned_by_seed(self):
        a = example()
        b = copy.deepcopy(a)
        b["folds"][0]["scenarios"] = [{"seed": 43, "ending_equity": 105},
                                      {"seed": 42, "ending_equity": 99}]
        result = compare(a, b)["folds"][0]
        self.assertAlmostEqual(result["left"]["max_drawdown_pct"], 10)
        self.assertEqual(result["left"]["fees"], 1.1)
        self.assertEqual(result["median_scenario_difference_pp"], -4)
        self.assertEqual(result["p05_scenario_difference_pp"], -10)
        self.assertEqual(result["share_paths_left_ahead"], .5)

    def test_assumptions_must_match(self):
        a = example()
        for key in ("fee_profile", "starting_cash", "engine_sha256"):
            b = copy.deepcopy(a)
            b["execution_contract"][key] = 200
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "Unmatched"):
                compare(a, b)
        b = copy.deepcopy(a)
        del b["execution_contract"]
        with self.assertRaisesRegex(ValueError, "regenerate"):
            compare(a, b)

    def test_no_subset_or_silent_truncation(self):
        a = example()
        b = copy.deepcopy(a)
        b["folds"][0]["end_exclusive"] = "2023-02-01"
        with self.assertRaisesRegex(ValueError, "dates"):
            compare(a, b)
        b = copy.deepcopy(a)
        b["folds"][0]["scenarios"][0]["seed"] = 43
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            compare(a, b)

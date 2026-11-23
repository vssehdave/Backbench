import unittest
from datetime import date

from controls import MeanThreshold, threshold
from harness import fees, fixture, replay, study
from stress import PathStress, StressConfig


class StressChecks(unittest.TestCase):
    rows = [(date(2022, 1, d), 100.0, close) for d, close in enumerate([110, 90, 110, 90], 1)]

    def test_delayed_target_uses_original_decision(self):
        _, _, fills = replay(self.rows, threshold, 100, (10000, 0), [110], 3, 0,
                             PathStress(100, 1, 0, 0))
        self.assertEqual([(t["date"], t["shares"]) for t in fills],
                         [("2022-01-02", 10), ("2022-01-04", -10)])

    def test_spread_and_costs_round_trip(self):
        state, _, fills = replay(self.rows[:3], threshold, 100, (10000, 0), [110], 3, 0,
                                 PathStress(100, 0, 100, 0))
        self.assertEqual([t["price"] for t in fills], [101, 99])
        self.assertEqual(state[1], 0)
        self.assertAlmostEqual(state[0], 9980 - sum(fees(10, 101)) - sum(fees(-10, 99)))

    def test_rejections_do_not_change_inventory(self):
        state, curve, fills = replay(self.rows, threshold, 100, (10000, 0), [110], 3, 0,
                                     PathStress(100, 0, 0, 1))
        self.assertEqual((state, curve, fills), ((10000, 0), [10000]*4, []))

    def test_neighbours_use_prefitted_artifacts_and_repeat(self):
        data = fixture()
        def run(config):
            return study(data, MeanThreshold, [-1, 0, 1], 12, 0, 1, date(2022,1,1),
                         date(2023,1,1), config)[0]
        result = run(StressConfig(neighbour_steps=1))
        paths = result["scenarios"]
        self.assertGreater(len({p["perturbations"]["level"] for p in paths}), 1)
        for path in paths:
            self.assertEqual(path["ending_equity"], result["sensitivity"][path["perturbations"]["level"]])
        bounds = StressConfig(2, 20, 0.15, 1)
        self.assertEqual(run(bounds), run(bounds))
        for path in run(StressConfig())["scenarios"]:
            self.assertEqual((path["added_fills"], path["removed_fills"], path["ending_delta_usd"]),
                             (0, 0, 0))

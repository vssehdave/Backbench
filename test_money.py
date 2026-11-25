import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
import harness
import money

GOOD = dict(id="pkg", version="1", entry="unseenpkg:decide", data=dict(kind="fixture", symbol="FIXTURE"),
            calendar="xnys", warmup=0, levels=[98, 100, 102], costs="equity_ibkr", benchmark="cash",
            max_exposure=1.0)
PACKAGE = '''
def decide(history, level):
    return 10 if history[-1] > level else None if history[-1] == level else 0
'''


def write(folder, manifest, name="m.json"):
    path = Path(folder) / name
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


class ManifestChecks(unittest.TestCase):
    def test_invalid_manifest_lists_every_problem(self):
        bad = dict(GOOD, entry="nothere:fn", calendar="utc24", warmup=-1, levels=[1, float("nan")],
                   max_exposure=2, version="")
        del bad["benchmark"]
        bad["extra"] = 1
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(money.ManifestError) as caught:
                money.load_manifest(write(folder, bad))
        message = str(caught.exception)
        for fragment in ("missing field: benchmark", "unknown field: extra", "version must", "warmup must",
                         "levels must", "max_exposure must", "cannot be imported", "calendar is 'utc24'"):
            self.assertIn(fragment, message)

    def test_spot_costs_must_match_calendar_and_be_finite(self):
        bad = dict(GOOD, costs=dict(fee_bps=float("inf"), lot=0.01, min_usd=10))
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "unseenpkg.py").write_text(PACKAGE)
            with self.assertRaises(money.ManifestError) as caught:
                money.load_manifest(write(folder, bad))
        self.assertIn("finite numbers", str(caught.exception))
        self.assertIn("calendar is 'xnys'", str(caught.exception))

    def test_unseen_package_runs_from_its_manifest_alone(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "unseenpkg.py").write_text(PACKAGE)
            manifest = money.load_manifest(write(folder, GOOD))
            report = money.run_test(manifest, date(2022, 7, 1), date(2023, 1, 1), 2, 5., 42)
        self.assertEqual(report["config"]["strategy"], "pkg")
        self.assertEqual(len(report["folds"]), 1)
        self.assertGreater(len(report["folds"][0]["fills"]), 0)


    def test_same_module_name_in_two_folders_loads_each_folders_own(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (Path(a) / "samename.py").write_text("def decide(history, level):\n    return 1\n")
            (Path(b) / "samename.py").write_text("def decide(history, level):\n    return 2\n")
            got = [money.Plugin(money.load_manifest(write(f, dict(GOOD, entry="samename:decide")))).inner((1.,), 0)
                   for f in (a, b)]
        self.assertEqual(got, [1, 2])


class FittedReplayChecks(unittest.TestCase):
    def test_fit_sees_only_pre_start_rows(self):
        fitted = []
        real = money.Plugin.__init__
        def spy(self, manifest):
            real(self, manifest)
            inner = self.fit
            self.fit = lambda rows, p: fitted.append(inner(rows, p)) or fitted[-1]
        money.Plugin.__init__ = spy
        self.addCleanup(setattr, money.Plugin, "__init__", real)
        manifest = money.load_manifest(Path("strategies/mean_threshold.json"))
        start, end = date(2022, 6, 1), date(2022, 8, 1)
        money.run_replay(manifest, start, end, 0.)
        real_rows = harness.fixture
        self.addCleanup(setattr, harness, "fixture", real_rows)
        harness.fixture = lambda: [(d, o * 3, c * 3) if d >= start else (d, o, c) for d, o, c in real_rows()]
        money.run_replay(manifest, start, end, 0.)
        self.assertEqual(fitted[0], fitted[1])

    def test_fitted_replay_without_prior_history_is_a_clear_error(self):
        manifest = money.load_manifest(Path("strategies/mean_threshold.json"))
        with self.assertRaisesRegex(ValueError, "history before --start"):
            money.run_replay(manifest, date(2022, 1, 1), date(2022, 3, 1), 0.)


class AbstentionChecks(unittest.TestCase):
    def test_none_holds_position_and_is_counted(self):
        rows = [(date(2023, 1, d), 100, 100) for d in range(1, 6)]
        script = iter([10, None, None, 0, None])
        log = {"abstentions": 0}
        state, _, fills = harness.replay(rows, lambda h, level: next(script), 0, (10000., 0), [100], log=log)
        self.assertEqual([t["shares"] for t in fills], [10, -10])
        self.assertEqual(state[1], 0)
        self.assertEqual(log["abstentions"], 3)
        script = iter([10, None, None])
        state, _, _ = harness.replay(rows[:3], lambda h, level: next(script), 0, (10000., 0), [100])
        self.assertEqual(state[1], 10)

    def test_delayed_abstention_does_not_revert_position(self):
        rows = [(date(2023, 1, d), 100, 100) for d in range(1, 6)]
        script = iter([10, None, None, None, None])
        stress = type("S", (), dict(delay_sessions=1, reject_probability=0., half_spread_bps=0.))()
        state, _, _ = harness.replay(rows, lambda h, level: next(script), 0, (10000., 0), [100], stress=stress)
        self.assertEqual(state[1], 10)


if __name__ == "__main__":
    unittest.main()

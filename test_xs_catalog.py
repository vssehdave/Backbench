import importlib.util
import json
import random
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import xsection as xs

CATALOG = Path(__file__).resolve().parent / "strategies" / "catalog"


def load(folder):
    spec = importlib.util.spec_from_file_location("xs_cat_" + folder.replace(".", "_").replace("-", "_"),
                                                  CATALOG / folder / "strategy_xs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decide


def curve(returns, start=100.):
    out = [start]
    for r in returns:
        out.append(out[-1] * (1 + r))
    return tuple(out)


def seen(prices, aux=None):
    n = len(next(iter(prices.values())))
    dates = tuple(date(2020, 1, 1) + timedelta(days=i) for i in range(n))
    return xs.AsOf(dates[-1], dates, prices, aux or {})


class Stocks(unittest.TestCase):
    def test_momentum_longs_the_winner_and_shorts_the_loser_skipping_the_last_bar(self):
        prices = {f"S{i}": curve([0.001 * i] * 9) for i in range(10)}
        # S0 is the worst but jumps on the final bar; the skipped bar must not rescue it.
        prices["S0"] = prices["S0"][:-1] + (prices["S0"][-1] * 3,)
        w = load("3.1-price-momentum")(seen(prices), dict(lookback=8, skip=1, share=0.1))
        self.assertEqual(w, {"S0": -0.5, "S9": 0.5})

    def test_low_volatility_is_long_calm_and_short_wild(self):
        prices = {f"S{i}": curve([0.01 * i * (-1) ** t for t in range(20)]) for i in range(1, 6)}
        w = load("3.4-low-volatility-anomaly")(seen(prices), dict(window=10, share=0.2))
        self.assertEqual(w, {"S1": 0.5, "S5": -0.5})

    def test_multifactor_needs_both_ranks(self):
        # A: best momentum and calmest; J: worst of both; the others sit between.
        prices = {n: curve([0.004 * (9 - i) + 0.002 * i * (-1) ** t for t in range(30)]) for i, n in enumerate("ABCDEFGHIJ")}
        w = load("3.6-multifactor-portfolio")(seen(prices), dict(lookback=20, skip=1, window=20, share=0.1))
        self.assertEqual(w, {"A": 0.5, "J": -0.5})

    def test_stat_arb_weights_are_neutral_normalised_and_signed_by_expected_return(self):
        prices = {"A": curve([0.002 + 0.001 * (-1) ** t for t in range(30)]),
                  "B": curve([0.000 + 0.001 * (-1) ** t for t in range(30)]),
                  "C": curve([-0.002 + 0.004 * (-1) ** t for t in range(30)])}
        w = load("3.18-statistical-arbitrage-optimization")(seen(prices), dict(lookback=20, skip=1, window=20))
        self.assertAlmostEqual(sum(w.values()), 0, places=12)
        self.assertAlmostEqual(sum(abs(x) for x in w.values()), 1, places=12)
        self.assertGreater(w["A"], 0)
        self.assertLess(w["C"], 0)

    def test_residual_momentum_ignores_the_market(self):
        rng = random.Random(3)
        names = [f"S{i}" for i in range(24)]
        market = [rng.gauss(0, 0.01) for _ in range(130)]
        rets = {s: [m + rng.gauss(0, 0.003) for m in market] for s in names}
        for k in range(130 - 84 - 1, 130 - 21 - 1):  # months 1 to 3 back; the skipped month stays flat
            rets["S0"][k] += 0.01
            rets["S1"][k] -= 0.01
        w = load("3.7-residual-momentum")(seen({s: curve(r) for s, r in rets.items()}), dict(S=1, T=3, W=5, share=0.05))
        self.assertEqual(w, {"S1": -0.5, "S0": 0.5})


class MeanReversion(unittest.TestCase):
    prices = {"A": (100., 110.), "B": (100., 100.), "C": (100., 90.), "X": (100., 120.)}
    sectors = {"A": "T", "B": "T", "C": "T", "X": "U"}

    def test_single_cluster_shorts_the_riser_and_is_neutral(self):
        w = load("3.9-mean-reversion-single-cluster")(seen(self.prices), dict(lookback=1))
        self.assertAlmostEqual(sum(w.values()), 0, places=12)
        self.assertAlmostEqual(sum(abs(x) for x in w.values()), 1, places=12)
        self.assertLess(w["X"], 0)
        self.assertGreater(w["C"], 0)

    def test_clusters_are_neutral_each_and_unclassified_names_are_dropped(self):
        prices = dict(self.prices, Z=(100., 150.))
        w = load("3.9.1-mean-reversion-multiple-clusters")(seen(prices), dict(lookback=1, sectors=self.sectors))
        self.assertNotIn("Z", w)
        self.assertEqual(w["X"], 0)  # alone in its cluster, so it is its own mean
        self.assertAlmostEqual(w["A"] + w["B"] + w["C"], 0, places=12)
        self.assertAlmostEqual(sum(abs(x) for x in w.values()), 1, places=12)
        self.assertLess(w["A"], 0)

    def test_weighted_regression_is_cluster_neutral_and_favours_calm_names(self):
        calm = curve([0.001 * (-1) ** t for t in range(19)] + [-0.05])
        wild = curve([0.03 * (-1) ** t for t in range(19)] + [-0.05])
        prices = {"A": calm, "B": wild, "C": curve([0.0] * 19 + [0.05]), "X": curve([0.001 * (-1) ** t for t in range(20)])}
        w = load("3.10-mean-reversion-weighted-regression")(seen(prices),
                                                             dict(lookback=1, window=15, sectors=self.sectors))
        self.assertAlmostEqual(w["A"] + w["B"] + w["C"], 0, places=12)
        self.assertGreater(abs(w["A"]), abs(w["B"]))  # equal returns, but the calm name has the larger z


class EtfRotation(unittest.TestCase):
    def test_sector_momentum_holds_the_top_sector(self):
        prices = {"X": curve([0.002] * 29), "Y": curve([0.001] * 29), "Z": curve([-0.001] * 29)}
        w = load("4.1-sector-momentum-rotation")(seen(prices), dict(T=1, share=0.1))
        self.assertEqual(w, {"X": 1.0})

    def test_ma_filter_goes_to_cash_when_the_leader_is_below_its_average(self):
        prices = {"X": curve([0.01] * 20 + [-0.04] * 4), "Y": curve([0.0] * 24)}  # X leads but sits under its 5-day MA
        decide = load("4.1.1-sector-momentum-rotation-with-ma-filter")
        self.assertEqual(decide(seen(prices), dict(T=1, ma=5, share=0.1)), {})
        self.assertEqual(decide(seen({"X": curve([0.01] * 24), "Y": prices["Y"]}), dict(T=1, ma=5, share=0.1)), {"X": 1.0})

    def test_dual_momentum_switches_to_the_safe_asset_when_spy_is_below_its_average(self):
        prices = {"X": curve([0.002] * 29), "Y": curve([0.001] * 29), "GLD": curve([0.0] * 29)}
        decide = load("4.1.2-dual-momentum-sector-rotation")
        p = dict(T=1, ma=5, share=0.1, safe="GLD")
        self.assertEqual(decide(seen(prices, {"SPY": curve([0.01] * 28 + [-0.1])}), p), {"GLD": 1.0})
        self.assertEqual(decide(seen(prices, {"SPY": curve([0.01] * 29)}), p), {"X": 1.0})

    def factors(self, n=40):
        rng = random.Random(5)
        r = {s: [rng.gauss(0, 0.01) for _ in range(n)] for s in ("SPY", "IWM", "IVE", "IVW", "MTUM")}
        return r, {s: curve(v) for s, v in r.items()}

    def test_alpha_rotation_picks_the_highest_intercept(self):
        r, aux = self.factors()
        prices = {"A": curve([0.002 + 0.8 * m for m in r["SPY"]]), "B": curve([0.8 * m for m in r["SPY"]]),
                  "C": curve([-0.002 + 0.8 * m for m in r["SPY"]])}
        w = load("4.2-alpha-rotation")(seen(prices, aux), dict(window=40, share=0.1))
        self.assertEqual(w, {"A": 1.0})

    def test_r_squared_is_long_low_r2_and_short_high_r2(self):
        r, aux = self.factors()
        rng = random.Random(9)
        prices = {"HIGH": curve([0.5 * m + 0.2 * q for m, q in zip(r["SPY"], r["MTUM"])]),
                  "MID1": curve([0.5 * m + rng.gauss(0, 0.01) for m in r["SPY"]]),
                  "MID2": curve([0.5 * m + rng.gauss(0, 0.02) for m in r["SPY"]]),
                  "MID3": curve([0.3 * m + rng.gauss(0, 0.02) for m in r["SPY"]]),
                  "LOW": curve([rng.gauss(0, 0.02) for _ in r["SPY"]])}
        w = load("4.3-r-squared")(seen(prices, aux), dict(window=40, share=0.2))
        self.assertEqual(w, {"LOW": 0.5, "HIGH": -0.5})


class Engine(unittest.TestCase):
    def test_same_module_name_in_two_folders_loads_each_strategy(self):
        with tempfile.TemporaryDirectory() as root:
            for name, weight in (("a", 0.1), ("b", 0.2)):
                folder = Path(root) / name
                folder.mkdir()
                (folder / "strategy_xs.py").write_text(f"def decide(panel, params):\n    return {{'X': {weight}}}\n")
                (folder / "m.json").write_text(json.dumps(dict(
                    id=name, version="1", entry="strategy_xs:decide", cadence="monthly", levels=[{}],
                    limits=dict(max_gross=1, max_net=1, name_cap=1), benchmark="SPY")))
            got = [xs.load_manifest(Path(root) / n / "m.json")[1][0](None, None)["X"] for n in ("a", "b", "a")]
        self.assertEqual(got, [0.1, 0.2, 0.1])

    def test_aux_series_are_truncated_at_the_decision_date(self):
        import xs_data
        dates = [date(2024, 1, 1) + timedelta(days=i) for i in range(10)]
        panel = xs_data.Panel(dates, {"A": [1.] * 10}, {"A": [1.] * 10})
        panel.aux = {"F": list(range(10))}
        self.assertEqual(xs.view(panel, 4).aux["F"], (0, 1, 2, 3, 4))
        self.assertNotIn("F", xs.view(panel, 4).prices)


if __name__ == "__main__":
    unittest.main()

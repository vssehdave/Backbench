"""Compare two forward-test reports with matching execution and data assumptions."""
import argparse
import json
import math
from pathlib import Path
from statistics import median
from stress import max_drawdown


def number(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("Expected a finite numeric measurement")
    return value


def settings(report):
    contract = report.get("execution_contract", {})
    for key in ("engine_sha256", "fee_profile", "starting_cash"):
        if not contract.get(key):
            raise ValueError(f"Missing execution_contract.{key}; regenerate the report")
    if number(contract["starting_cash"]) <= 0:
        raise ValueError("Starting capital must be positive")
    config = report["config"]
    for key in ("start", "end", "symbol", "paths", "seed", "shock_bps"):
        if key not in config:
            raise ValueError(f"Missing research setting: {key}")
    ignore = {"strategy", "levels", "out", "provider", "minute_csv"}
    return {
        "execution_contract": contract,
        "source": report["source"],
        "currency": report["currency"],
        "data_sha256": report["data_sha256"],
        **{f"config.{k}": v for k, v in config.items() if k not in ignore},
    }


def fold_metrics(fold, capital):
    equity = fold["equity"]
    if not equity:
        raise ValueError("Empty forward equity series")
    drawdown = max_drawdown(map(number, equity), capital)
    net_return = equity[-1] / capital - 1
    if not math.isclose(net_return, number(fold["forward_return"]), abs_tol=1e-10):
        raise ValueError("Forward return and marked equity disagree")
    fees = sum(number(t["commission"]) + number(t["regulatory"]) for t in fold["fills"])
    return {
        "selected_parameter": fold["selected"],
        "selection_start": fold["selection_start"],
        "selection_return_pct": 100 * number(fold["selection_return"]),
        "forward_return_pct": 100 * net_return,
        "max_drawdown_pct": 100 * drawdown,
        "fees": fees,
        "fills": len(fold["fills"]),
    }


def scenarios_by_seed(fold, expected):
    paths = fold["scenarios"]
    values = {p["seed"]: number(p["ending_equity"]) for p in paths}
    if not expected or len(paths) != expected or len(values) != expected:
        raise ValueError("Duplicate or missing Monte Carlo paths")
    return values


def compare(left, right):
    setup = settings(left)
    other = settings(right)
    mismatches = sorted(k for k in setup.keys() | other.keys() if setup.get(k) != other.get(k))
    if mismatches:
        raise ValueError("Unmatched runs: " + ", ".join(mismatches))
    if not left["folds"] or len(left["folds"]) != len(right["folds"]):
        raise ValueError("Unequal or empty fold coverage")
    capital = setup["execution_contract"]["starting_cash"]
    results = []
    for a, b in zip(left["folds"], right["folds"]):
        bounds = ("train_start", "forward_start", "end_exclusive")
        if any(a[k] != b[k] for k in bounds) or len(a["equity"]) != len(b["equity"]):
            raise ValueError("Unmatched fold dates or session count")
        ma, mb = fold_metrics(a, capital), fold_metrics(b, capital)
        pa = scenarios_by_seed(a, left["config"]["paths"])
        pb = scenarios_by_seed(b, right["config"]["paths"])
        if pa.keys() != pb.keys():
            raise ValueError("Unmatched scenario seeds")
        deltas = sorted(100 * (pa[s] - pb[s]) / capital for s in pa)
        results.append({
            **{k: a[k] for k in bounds}, "sessions": len(a["equity"]),
            "left": ma, "right": mb,
            "forward_difference_pp": ma["forward_return_pct"] - mb["forward_return_pct"],
            "paired_paths": len(deltas),
            "median_scenario_difference_pp": median(deltas),
            "p05_scenario_difference_pp": deltas[math.ceil(len(deltas) * .05) - 1],
            "share_paths_left_ahead": sum(d > 0 for d in deltas) / len(deltas),
        })
    return {"currency": setup["currency"], "left": left["config"]["strategy"],
            "right": right["config"]["strategy"], "folds": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    args = parser.parse_args()
    try:
        reports = [json.loads(p.read_text(encoding="utf-8")) for p in (args.left, args.right)]
        result = compare(*reports)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Cannot compare: {exc}\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

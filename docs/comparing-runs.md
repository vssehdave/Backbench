# Comparing matched research runs

Run both strategies with the same runner revision, input data, date range, asset, fees, starting capital, path count, seed and shock size. Strategy identifiers, candidate parameters, file locations and output names may differ. The data hash identifies the observations supplied to the engine.

```sh
python harness.py --strategy controls:threshold --levels 98 100 102 --out threshold.json
python harness.py --strategy controls:MeanThreshold --levels -1 0 1 --out fitted.json
python compare.py fitted.json threshold.json
```

The command prints JSON to stdout and reports incompatible inputs on stderr with exit status 2. Reports predating the execution contract must be regenerated. An identical engine digest intentionally provides a conservative check when fee, fill, scaling or accounting code changes.

Each six-month forward fold is an independent comparison. Returns and drawdowns use the recorded opening capital. Maximum drawdown includes the drop from that opening capital to the first mark. Fees sum the commission and regulatory charges already reflected in equity. The selection start date gives context when fitted and rule-based strategies used different inner training windows.

The paired Monte Carlo differences subtract the right strategy's ending equity from the left strategy's for the same seed and divide by initial capital. Values are percentage points. The report shows the median difference, fifth percentile using nearest rank, and fraction of paths where the left strategy finishes ahead. A tie contributes zero to that fraction. These are outcomes under the configured perturbation model. Short forward samples and a small path count limit precision. No pooling or compounding across disjoint folds is performed.

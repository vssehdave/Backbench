# Monte Carlo risk

Every strategy result now carries a distribution of max drawdown, not only the one historical number. Code: `montecarlo.py` (bootstrap and statistics), `mc_runs.py` (the three engines), `report.py` (REPORT.md and trade logs). Run it with:

```
python money.py mc <manifest> [--paths 1000] [--seed 0] [--block 20]
```

The manifest picks the engine: a `cadence` field means a cross-section manifest (200 paths by default), `"runner": "options_bt.py"` means an option strategy, anything else is the single-instrument harness. The existing execution stress (delay, spread, rejects, shock, neighbouring parameters) is unchanged and still runs; the Monte Carlo is layered on top and the benchmark gets the same treatment.

## Method

- **Stationary block bootstrap** (Politis and Romano): the next index continues the current block, or with probability 1/20 starts a new block at a random place, so block lengths are geometric with mean 20 sessions. Seeded per fold and path from a string, so a run is exactly repeatable.
- **Mode A, path rerun** (harness, cross-section). Per walk-forward fold, the forward window is replaced by a synthetic one built from bootstrapped returns and the strategy is re-run with its normal costs. The strategy's history is the real training data; the synthetic path is glued on at the last real close. Single instrument: whole bars are resampled (overnight gap and open-to-close move together). Cross-section: whole dates are resampled across all stocks jointly, so cross-correlation is kept; a stock with no bar on a drawn date takes the day's equal-weight mean return. Per-fold curves are chained into one curve per path (about 10 folds of six months each for the harness).
- **Mode B, P&L bootstrap** (options, and usable anywhere): block-bootstrap the strategy's own daily equity returns over the whole test period. No repricing, so no implied-volatility history is needed.
- **Statistics per series**: max drawdown p5/p50/p95/p99, the historical max drawdown with its percentile rank inside the simulated distribution, P(DD>20/30/50%), longest and average share of time under water, and terminal return percentiles. The benchmark gets the same run.

## Limits

- The pool is 2016-2026 only. A path cannot contain a move worse than what a resampled block contains, so the tail is bounded by the worst historical days and blocks (2020, 2022). p99 is not a worst case.
- Resampling blocks of 20 sessions keeps short volatility clustering but not regimes (a year-long bear market, a rate shock, momentum crashes that unfold over months). A strategy whose real drawdown was a slow regime event will rank high against its own distribution: xs momentum_12_1 sits at the 97th percentile.
- Windows are the walk-forward out-of-sample windows, not the whole decade. The single-instrument harness trains for six months and trades the next six, once per year, so the reported historical drawdown (SPY 10.2%) is for those windows only and excludes, for example, February-March 2020. That is why it is far below SPY's full-history drawdown. The benchmark column uses the same windows, so comparisons are like for like.
- Fold chaining: simulated folds are independent draws chained together; carry-over between folds is only through equity, which is the same as the real run.
- Mode B ignores path-dependent gamma: a covered call or protective put is resampled as a return stream, so how the option payoff would respond to a different path is not modelled, and the bootstrapped stream still carries the historical sequence of strikes and assignments. Treat options results as a statement about the realized P&L stream (34 monthly cycles, about two years), not about the strategy in general.
- Daily log returns are resampled with no drift adjustment, so simulated terminal returns reflect the sample's own drift.

## Results

SPY and catalog runs use 1000 paths, cross-section runs 200. Seed 0, mean block 20. Rank is the percentile of the historical max drawdown inside the simulated distribution.

| strategy | series | historical max DD (pct rank) | MC p50 | p95 | p99 | P(DD>20/30/50%) | terminal return p50 | paths | runtime |
|---|---|---|---|---|---|---|---|---|---|
| cat-2.2-covered-call-options | strategy | 16.3% (rank 67) | 14.1% | 24.5% | 29.1% | 14.7% / 0.8% / 0.0% | 34.5% (hist 33.7%) | 1000 | 1s |
| cat-2.2-covered-call-options | benchmark | 18.5% (rank 61) | 16.6% | 28.2% | 33.3% | 27.4% / 2.8% / 0.0% | 41.9% (hist 41.5%) | 1000 | 1s |
| cat-2.4-protective-put-options | strategy | 14.1% (rank 55) | 13.9% | 23.4% | 29.0% | 12.4% / 0.6% / 0.0% | 32.5% (hist 32.5%) | 1000 | 1s |
| cat-2.4-protective-put-options | benchmark | 18.5% (rank 61) | 16.6% | 28.2% | 33.3% | 27.4% / 2.8% / 0.0% | 41.9% (hist 41.5%) | 1000 | 1s |
| cat-3.12-two-moving-averages | strategy | 6.9% (rank 11) | 10.5% | 18.6% | 23.0% | 3.0% / 0.0% / 0.0% | 20.8% (hist 23.4%) | 1000 | 70s |
| cat-3.12-two-moving-averages | benchmark | 10.2% (rank 27) | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 41.1% (hist 46.8%) | 1000 | 70s |
| cat-3.12-two-moving-averages-long-short | strategy | 12.0% (rank 11) | 18.5% | 33.8% | 40.8% | 41.1% / 10.5% / 0.0% | 3.4% (hist 2.8%) | 1000 | 71s |
| cat-3.12-two-moving-averages-long-short | benchmark | 10.2% (rank 27) | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 41.1% (hist 46.8%) | 1000 | 71s |
| cat-6.5-index-volatility-targeting | strategy | 6.6% (rank 20) | 8.5% | 14.7% | 18.4% | 0.8% / 0.0% / 0.0% | 26.3% (hist 34.6%) | 1000 | 84s |
| cat-6.5-index-volatility-targeting | benchmark | 10.2% (rank 27) | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 41.1% (hist 46.8%) | 1000 | 84s |
| bench-buy-and-hold-spy | strategy | 10.2% (rank 27) | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 41.1% (hist 46.8%) | 1000 | 71s |
| bench-buy-and-hold-spy | benchmark | 10.2% (rank 27) | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 41.1% (hist 46.8%) | 1000 | 71s |
| xs_low_volatility | strategy | 14.2% (rank 30) | 18.1% | 36.7% | 43.3% | 40.0% / 22.5% / 0.5% | 67.4% (hist 65.6%) | 200 | 3489s |
| xs_low_volatility | benchmark (SPY) | 19.3% (rank 29) | 23.1% | 39.0% | 50.9% | 67.5% / 29.0% / 1.5% | 103.5% (hist 125.2%) | 200 | 3489s |
| xs_momentum_12_1 | strategy | 30.2% (rank 97) | 15.3% | 27.9% | 34.7% | 27.5% / 3.5% / 0.5% | 15.1% (hist -11.8%) | 200 | 591s |
| xs_momentum_12_1 | benchmark (SPY) | 19.3% (rank 29) | 23.1% | 39.0% | 50.9% | 67.5% / 29.0% / 1.5% | 103.5% (hist 125.2%) | 200 | 591s |

Per-strategy READMEs have the same numbers, `mc_results*.json` beside each manifest holds the full detail (all percentiles, underwater distribution, terminal return percentiles), and `results/` holds REPORT.md and trade logs.

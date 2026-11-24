# xs

## Monte Carlo risk

A: path rerun on jointly bootstrapped dates; 200 paths, seed 0, mean block 20.0 sessions, 637s. Method and limits: docs/monte-carlo.md. Raw numbers: `mc_results_momentum_12_1.json`; report and trade logs in the `results/` folder beside it.

| series | historical max DD (pct rank) | MC p50 | p95 | p99 | P(DD>20/30/50%) | terminal return p50 |
|---|---|---|---|---|---|---|
| strategy | 30.2% (rank 97) | 15.3% | 27.9% | 34.7% | 27.5% / 3.5% / 0.5% | 15.1% (hist -11.8%) |
| benchmark (SPY) | 19.3% (rank 29) | 23.1% | 39.0% | 50.9% | 67.5% / 29.0% / 1.5% | 103.5% (hist 125.2%) |
<!-- mc:mc_results_momentum_12_1 -->

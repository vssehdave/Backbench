# 2.4 Protective put

- Section: 2.4
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Long 200 SPY shares, each month buy 2 put contracts about 5% OTM, ~30 DTE (next third-Friday expiry), held to expiry. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy (a.k.a. "married put" or "synthetic call") amounts to buying stock and an ATM or OTM put option with a strike price K ≤ S 0. The trader's outlook is bullish. This is a hedging strategy: the put option hedges the risk of the stock price falling. We have: 13

fT = ST −S0 + (K −ST)+ −D = K −S0 + (ST −K)+ −D (9) $$ S∗= S0 + D $$ (10) *P max = unlimited (11) Lmax = S0 −K + D (12)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| protective put | 32.5% | -14.1% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 4, assignments 0, fees USD 44.20, missing-bar days 2, mark gaps 1. Return at half-spreads 0 / 0.05 / 0.10: 32.6% / 32.3% / 31.9%.

## Monte Carlo risk

B: path rerun; 1000 paths, seed 0, mean block 20.0 sessions, 1s. Method and limits: docs/monte-carlo.md. Raw numbers: `mc_results.json`; report and trade logs in the `results/` folder beside it.

| series | historical max DD (pct rank) | MC p50 | p95 | p99 | P(DD>20/30/50%) | terminal return p50 |
|---|---|---|---|---|---|---|
| strategy | 14.1% (rank 55) | 13.9% | 23.4% | 29.0% | 12.4% / 0.6% / 0.0% | 32.5% (hist 32.5%) |
| benchmark | 18.5% (rank 60) | 16.6% | 28.2% | 33.3% | 27.4% / 2.8% / 0.0% | 41.9% (hist 41.5%) |
<!-- mc:mc_results -->

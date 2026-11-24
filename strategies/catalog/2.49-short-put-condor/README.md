# 2.49 Short put condor

- Section: 2.49
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n put contracts at spot*0.9625; long 1 x n put contracts at spot*0.9875; long 1 x n put contracts at spot*1.0125; short 1 x n put contracts at spot*1.0375. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a short position in an OTM put option with a strike price K 1, a long position in an OTM put option with a higher strike price K 2, a long position in an ITM put option with a strike price K 3, and a short position in an ITM put option with a higher strike price K 4. All strikes are equidistant: *K 4 − K 3 = K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low net credit trade.

As with a short put butterfly, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). So, this is a capital gain (rather than an income) strategy. The trader's outlook is neutral. We have:

$$ fT = (K2 −ST)+ + (K3 −ST)+ −(K1 −ST)+ −(K4 −ST)+ + C $$ (221) *S ∗ up = K 4 − C (222) S∗down = K1 + C (223) *P max = C (224) Lmax = \kappa −C (225)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.49. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short put condor | -13.9% | -22.7% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 57, assignments 33, fees USD 176.80, missing-bar days 81, mark gaps 139. Return at half-spreads 0 / 0.05 / 0.10: -13.3% / -14.7% / -16.0%.

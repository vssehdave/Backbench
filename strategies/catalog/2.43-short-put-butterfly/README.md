# 2.43 Short put butterfly

- Section: 2.43
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n put contracts at spot*0.9750; long 2 x n put contracts at spot*1.0000; short 1 x n put contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a short position in an ITM put option with a strike price K 1, a long position in two ATM put options with a strike price K 2, and a short position in an OTM put option with a strike price K 3. The strikes are equidistant: K 2 − K 3 = K 1 − K 2 = κ. This is a net credit trade. In this sense, this is an income strategy. However, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). The trader's outlook is neutral. We have:

$$ fT = 2 \times (K2 −ST)+ −(K1 −ST)+ −(K3 −ST)+ + C $$ (191) S∗down = K3 + C (192) *S ∗ up = K 1 − C (193) *P max = C (194) Lmax = \kappa −C (195)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.43. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short put butterfly | -12.5% | -21.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 35, assignments 26, fees USD 176.80, missing-bar days 30, mark gaps 51. Return at half-spreads 0 / 0.05 / 0.10: -12.0% / -13.3% / -14.7%.

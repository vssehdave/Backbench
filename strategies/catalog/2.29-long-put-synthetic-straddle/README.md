# 2.29 Long put synthetic straddle

- Section: 2.29
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 100 x n shares; long 2 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This volatility strategy (which is the same as a long straddle with the call replaced by a synthetic call) amounts to buying stock and buying two ATM (or the nearest ITM) put options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming S 0 ≤ K and D \> K − S 0 ):

$$ fT = ST −S0 + 2 \times (K −ST)+ −D $$ (116) S∗up = S0 + D (117) S∗down = 2 \times K −S0 −D (118) *P max = unlimited (119) Lmax = D −(K −S0) (120)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.29. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long put synthetic straddle | -0.9% | -19.7% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 9, assignments 0, fees USD 88.40, missing-bar days 2, mark gaps 1. Return at half-spreads 0 / 0.05 / 0.10: -0.7% / -1.3% / -2.0%.

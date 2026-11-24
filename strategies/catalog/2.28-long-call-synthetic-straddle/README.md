# 2.28 Long call synthetic straddle

- Section: 2.28
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 100 x n shares; long 2 x n call contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This volatility strategy (which is the same as a long straddle with the put replaced by a synthetic put) amounts to shorting stock and buying two ATM (or the nearest ITM) call options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. 25 We have (assuming S 0 ≥ K and D \> S 0 − K):

$$ fT = S0 −ST + 2 \times (ST −K)+ −D $$ (111) S∗up = 2 \times K −S0 + D (112) *S ∗ down = S 0 − D (113) *P max = unlimited (114) Lmax = D −(S0 −K) (115)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.28. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long call synthetic straddle | -29.5% | -43.0% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 25, assignments 0, fees USD 88.40, missing-bar days 2, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: -29.2% / -29.9% / -30.6%.

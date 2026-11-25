# 2.30 Short call synthetic straddle

- Section: 2.30
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 100 x n shares; short 2 x n call contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This sideways strategy (which is the same as a short straddle with the put replaced by a synthetic put) amounts to buying stock and selling two ATM (or the nearest

OTM) call options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming S 0 ≤ K):

$$ fT = ST −S0 −2 \times (ST −K)+ + C $$ (121) S∗up = 2 \times K −S0 + C (122) *S ∗ down = S 0 − C (123) Pmax = K −S0 + C (124) *L max = unlimited (125)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.30. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short call synthetic straddle | 28.8% | -11.2% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 25, assignments 25, fees USD 88.40, missing-bar days 2, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: 29.0% / 28.4% / 27.7%.

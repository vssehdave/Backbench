# 2.25 Short straddle

- Section: 2.25
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n call contracts at spot*1.0000; short 1 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This a is sideways strategy consisting of a short position in an ATM call option, and a short position in an ATM put option with a strike price K. This is a net credit trade. The trader's outlook is neutral. This is an income strategy. We have:

fT = −(ST −K)+ −(K −ST)+ + C (96) S∗up = K + C (97) *S ∗ down = K − C (98) *P max = C (99) *L max = unlimited (100)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.25. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short straddle | 14.5% | -12.7% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 34, fees USD 88.40, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: 14.8% / 14.1% / 13.4%.

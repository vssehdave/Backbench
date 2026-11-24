# 2.32 Covered short straddle

- Section: 2.32
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 100 x n shares; short 1 x n call contracts at spot*1.0000; short 1 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy amounts to augmenting a covered call by writing a put option with the same strike price K and TTM as the sold call option and thereby increasing the income. The trader's outlook is bullish. We have:

fT = ST −S0 −(ST −K)+ −(K −ST)+ + C (131)

S∗= 1

2 ( S 0 + K − C ) (132) Pmax = K −S0 + C (133) Lmax = S0 + K −C (134)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.32. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| covered short straddle | 56.0% | -24.3% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 34, fees USD 88.40, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: 56.2% / 55.6% / 54.9%.

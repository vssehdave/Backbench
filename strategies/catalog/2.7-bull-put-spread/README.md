# 2.7 Bull put spread

- Section: 2.7
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*0.9500; short 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a vertical spread consisting of a long position in an OTM put option with a strike price K 1, and a short position in another OTM put option with a higher strike price K 2. This is a net credit trade. The trader's outlook is bullish. This is an income strategy. We have:

fT = (K1 −ST)+ −(K2 −ST)+ + C

(21) S∗= K2 −C (22) *P max = C (23) Lmax = K2 −K1 −C (24)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bull put spread | 1.7% | -5.0% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 9, assignments 5, fees USD 88.40, missing-bar days 3, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: 2.0% / 1.3% / 0.7%.

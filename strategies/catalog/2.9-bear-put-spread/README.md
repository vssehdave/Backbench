# 2.9 Bear put spread

- Section: 2.9
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*1.0000; short 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a vertical spread consisting of a long position in a close to ATM put option with a strike price K 1, and a short position in an OTM put option with a lower

strike price K 2. This is a net debit trade. The trader's outlook is bearish: this strategy profits if the stock price falls. This is a capital gain strategy. We have:

fT = (K1 −ST)+ −(K2 −ST)+ −D

(29) S∗= K1 −D (30) Pmax = K1 −K2 −D (31) *L max = D (32)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.9. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bear put spread | -10.5% | -14.0% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 14, assignments 5, fees USD 88.40, missing-bar days 3, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: -10.2% / -10.9% / -11.6%.

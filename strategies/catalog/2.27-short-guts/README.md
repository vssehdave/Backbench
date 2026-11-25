# 2.27 Short guts

- Section: 2.27
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n call contracts at spot*0.9750; short 1 x n put contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a sideways strategy consisting of a short position in an ITM call option with a strike price K 1, and a short position in an ITM put option with a strike price *K 2. This is a net credit trade. Since both call and put options are ITM, the initial

credit is higher than in a short straddle position. The flipside is that the risk is also higher. The trader's outlook is neutral. This is an income strategy. We have: 24

$$ fT = −(ST −K1)+ −(K2 −ST)+ + C $$ (106) S∗up = K1 + C (107) *S ∗ down = K 2 − C (108) Pmax = C −(K2 −K1) (109) *L max = unlimited (110)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.27. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short guts | 2.2% | -14.2% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 50, assignments 50, fees USD 88.40, missing-bar days 33, mark gaps 102. Return at half-spreads 0 / 0.05 / 0.10: 2.4% / 1.8% / 1.1%.

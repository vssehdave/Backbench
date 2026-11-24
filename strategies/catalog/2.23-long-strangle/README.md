# 2.23 Long strangle

- Section: 2.23
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0250; long 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a long position in an OTM call option with a strike price K 1, and a long position in an OTM put option with a strike price K 2. This is a net debit trade. However, because both call and put options are OTM, this strategy is less costly to establish than a long straddle position. The flipside is that the movement in the stock price required to reach one of the break-even points is also more significant. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (ST −K1)+ + (K2 −ST)+ −D $$ (86) S∗up = K1 + D (87) *S ∗ down = K 2 − D (88) *P max = unlimited (89) *L max = D (90)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.23. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long strangle | -3.4% | -15.9% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 18, assignments 0, fees USD 88.40, missing-bar days 20, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: -3.1% / -3.8% / -4.5%.

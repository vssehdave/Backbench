# 2.22 Long straddle

- Section: 2.22
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0000; long 1 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a long position in an ATM call option, and a long position in an ATM put option with a strike price K. This is a net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have 22:

$$ fT = (ST −K)+ + (K −ST)+ −D $$ (81) S∗up = K + D (82) *S ∗ down = K − D (83) *P max = unlimited (84) *L max = D (85)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.22. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long straddle | -15.2% | -30.8% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 0, fees USD 88.40, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: -14.9% / -15.6% / -16.3%.

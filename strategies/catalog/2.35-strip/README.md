# 2.35 Strip

- Section: 2.35
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0000; long 2 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a long position in an ATM call option, and a long position in two ATM put options with a strike price K. This is a net debit trade. The trader's outlook is bearish. This is a capital gain strategy. We have:

$$ fT = (ST −K)+ + 2 \times (K −ST)+ −D $$ (143) S∗up = K + D (144) *S ∗ down = K − D (145)

*P max = unlimited (146) *L max = D (147)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.35. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| strip | -36.4% | -63.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 0, fees USD 132.60, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: -36.0% / -37.0% / -38.0%.

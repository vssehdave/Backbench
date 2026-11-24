# 2.34 Strap

- Section: 2.34
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 2 x n call contracts at spot*1.0000; long 1 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a long position in two ATM call options, and a long position in an ATM put option with a strike price K. This is a net debit trade. The trader's outlook is bullish. This is a capital gain strategy. We have: 26

$$ fT = 2 \times (ST −K)+ + (K −ST)+ −D $$ (138) S∗up = K + D (139)

*S ∗ down = K − D (140) *P max = unlimited (141) *L max = D (142)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.34. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| strap | -9.2% | -30.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 0, fees USD 132.60, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: -8.8% / -9.8% / -10.9%.

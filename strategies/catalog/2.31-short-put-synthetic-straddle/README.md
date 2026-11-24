# 2.31 Short put synthetic straddle

- Section: 2.31
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 100 x n shares; short 2 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This sideways strategy (which is the same as a short straddle with the call replaced by a synthetic call) amounts to shorting stock and selling two ATM (or the nearest OTM) put options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming S 0 ≥ K):

$$ fT = S0 −ST −2 \times (K −ST)+ + C $$ (126) S∗up = S0 + C (127) S∗down = 2 \times K −S0 −C (128) Pmax = S0 −K + C (129) *L max = unlimited (130)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.31. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short put synthetic straddle | 0.2% | -14.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 9, assignments 9, fees USD 88.40, missing-bar days 2, mark gaps 1. Return at half-spreads 0 / 0.05 / 0.10: 0.5% / -0.2% / -0.9%.

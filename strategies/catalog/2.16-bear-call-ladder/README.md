# 2.16 Bear call ladder

- Section: 2.16
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n call contracts at spot*1.0000; long 1 x n call contracts at spot*1.0250; long 1 x n call contracts at spot*1.0500. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a vertical spread consisting of a short position in (usually) a close to ATM call option with a strike price K 1, a long position in an OTM call option with a strike price K 2, and a long position in another OTM call option with a higher strike price *K 3. A bear call ladder typically arises when a bear call spread (a bearish strategy) goes wrong (the stock trades higher), so the trader buys another OTM call option (with the strike price K 3 ) to adjust the position to bullish. We have:

$$ fT = (ST −K3)+ + (ST −K2)+ −(ST −K1)+ −H $$ (63) *S ∗ down = K 1 − H, H < 0 (64) $$ S∗up = K3 + K2 −K1 + H $$ (65) *P max = unlimited (66) Lmax = K2 −K1 + H (67)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.16. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bear call ladder | 12.0% | -6.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 42, assignments 25, fees USD 132.60, missing-bar days 172, mark gaps 10. Return at half-spreads 0 / 0.05 / 0.10: 12.4% / 11.4% / 10.4%.

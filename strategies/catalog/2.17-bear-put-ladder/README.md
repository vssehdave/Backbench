# 2.17 Bear put ladder

- Section: 2.17
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*1.0000; short 1 x n put contracts at spot*0.9750; short 1 x n put contracts at spot*0.9500. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a vertical spread consisting of a long position in (usually) a close to ATM put option with a strike price K 1, a short position in an OTM put option with a strike price K 2, and a short position in another OTM put option with a lower strike price K 3. A bear put ladder is a bear put spread financed by selling another OTM put option (with the strike price K 3 ). 20 This adjusts the trader's outlook from bearish (bear put spread) to conservatively bearish or even non-directional (with an

expectation of low volatility). We have (assuming K 3 + K 2 − K 1 + H \> max( *H, 0)):

$$ fT = (K1 −ST)+ −(K2 −ST)+ −(K3 −ST)+ −H $$ (68) *S ∗ up = K 1 − H, H > 0 (69) S∗down = K3 + K2 −K1 + H (70) Pmax = K1 −K2 −H (71) $$ Lmax = K3 + K2 −K1 + H $$ (72)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.17. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bear put ladder | -1.8% | -8.7% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 18, assignments 9, fees USD 132.60, missing-bar days 5, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: -1.4% / -2.4% / -3.5%.

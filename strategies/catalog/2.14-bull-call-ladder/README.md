# 2.14 Bull call ladder

- Section: 2.14
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0000; short 1 x n call contracts at spot*1.0250; short 1 x n call contracts at spot*1.0500. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a vertical spread consisting of a long position in (usually) a close to ATM call option with a strike price K 1, a short position in an OTM call option with a strike price K 2, and a short position in another OTM call option with a higher strike price K 3. A bull call ladder is a bull call spread financed by selling another OTM call option (with the strike price K 3 ). 18 This adjusts the trader's outlook from bullish (bull call spread) to conservatively bullish or even non-directional (with an expectation of low volatility). We have:

$$ fT = (ST −K1)+ −(ST −K2)+ −(ST −K3)+ −H $$ (53) S∗down = K1 + H, H > 0 (54) S∗up = K3 + K2 −K1 −H (55) Pmax = K2 −K1 −H (56) *L max = unlimited (57)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.14. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bull call ladder | -13.1% | -18.3% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 42, assignments 17, fees USD 132.60, missing-bar days 172, mark gaps 10. Return at half-spreads 0 / 0.05 / 0.10: -12.7% / -13.7% / -14.7%.

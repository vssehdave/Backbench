# 2.53 Collar

- Section: 2.53
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 100 x n shares; long 1 x n put contracts at spot*0.9500; short 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy (a.k.a. "fence") is a covered call augmented by a long put option as insurance against the stock price falling. 32 It amounts to buying stock, buying an OTM put option with a strike price K 1, and selling an OTM call option with a higher strike price K 2. The trader's outlook is moderately bullish. This is a capital gain strategy. We have: 33

fT = ST −S0 + (K1 −ST)+ −(ST −K2)+ −H

(238) $$ S∗= S0 + H $$ (239) Pmax = K2 −S0 −H (240) Lmax = S0 −K1 + H (241)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.53. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| collar | 24.4% | -11.8% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 17, assignments 13, fees USD 88.40, missing-bar days 21, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: 24.7% / 24.0% / 23.3%.

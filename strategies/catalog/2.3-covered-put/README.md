# 2.3 Covered put

- Section: 2.3
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 100 x n shares; short 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy (a.k.a. "sell-write" strategy) amounts to shorting stock and writing a put option with a strike price K against the stock position. The trader's outlook is

neutral to bearish. The covered put strategy has the same payoffas writing a call option (short/naked call). While maintaining the short stock position, the trader can generate income by periodically selling OTM put options. We have: 12

fT = S0 −ST −(K −ST)+ + C = S0 −K −(ST −K)+ + C (5) $$ S∗= S0 + C $$ (6) Pmax = S0 −K + C (7) *L max = unlimited (8)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| covered put | -30.7% | -41.0% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 5, assignments 5, fees USD 44.20, missing-bar days 1, mark gaps 1. Return at half-spreads 0 / 0.05 / 0.10: -30.6% / -30.9% / -31.3%.

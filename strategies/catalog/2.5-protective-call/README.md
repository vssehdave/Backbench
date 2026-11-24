# 2.5 Protective call

- Section: 2.5
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 100 x n shares; long 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy (a.k.a. "married call" or "synthetic put") amounts to shorting stock and buying an ATM or OTM call option with a strike price K ≥ S 0. The trader's outlook is bearish. This is a hedging strategy: the call option hedges the risk of the stock price rising. We have: 14

fT = S0 −ST + (ST −K)+ −D = S0 −K + (K −ST)+ −D

(13) S∗= S0 −D (14) *P max = S 0 − D (15) Lmax = K −S0 + D (16)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| protective call | -33.8% | -49.9% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 13, assignments 0, fees USD 44.20, missing-bar days 19, mark gaps 1. Return at half-spreads 0 / 0.05 / 0.10: -33.7% / -34.0% / -34.3%.

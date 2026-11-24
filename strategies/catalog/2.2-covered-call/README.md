# 2.2 Covered call

- Section: 2.2
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Long 200 SPY shares, each month sell 2 call contracts about 2% OTM, ~30 DTE (next third-Friday expiry), held to expiry. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy (a.k.a. "buy-write" strategy) amounts to buying stock and writing a call option with a strike price K against the stock position. The trader's outlook on the stock price is neutral to bullish. The covered call strategy has the same payoffas writing a put option (short/naked put). 10 While maintaining the long stock position, the trader can generate income by periodically selling OTM call options. We have: 11

fT = ST −S0 −(ST −K)+ + C = K −S0 −(K −ST)+ + C

(1) S∗= S0 −C (2) Pmax = K −S0 + C (3) *L max = S 0 − C (4)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only.

| | Total return | Max drawdown |
|---|---|---|
| covered call | 33.7% | -16.3% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM expiries 13, assignments 13, fees USD 44.20, missing-bar days 3 (entry slipped), mark gaps 1. Return at half-spreads 0 / 0.05 / 0.10: 33.9% / 33.5% / 33.2%.

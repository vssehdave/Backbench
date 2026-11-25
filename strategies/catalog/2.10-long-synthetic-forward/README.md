# 2.10 Long synthetic forward

- Section: 2.10
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0000; short 1 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy amounts to buying an ATM call option and selling an ATM put option with a strike price K = S 0. This can be a net debit or net credit trade. Typically, *\| H \| ≪ S 0. The trader's outlook is bullish: this strategy mimics a long stock or futures position; it replicates a long forward contract with the delivery price K and the same maturity as the options. This is a capital gain strategy. We have: 16

fT = (ST −K)+ −(K −ST)+ −H = ST −K −H (33) S∗= K + H (34) *P max = unlimited (35) Lmax = K + H (36)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.10. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long synthetic forward | 26.8% | -20.0% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 9, fees USD 88.40, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: 27.1% / 26.4% / 25.7%.

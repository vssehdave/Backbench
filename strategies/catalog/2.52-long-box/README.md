# 2.52 Long box

- Section: 2.52
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*0.9750; short 1 x n call contracts at spot*1.0250; long 1 x n put contracts at spot*1.0250; short 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This volatility strategy can be viewed as a combination of a long synthetic forward and a short synthetic forward, or as a combination of a bull call spread and a bear put spread, and consists of a long position in an ITM put option with a strike price *K 1, a short position in an OTM put option with a lower strike price K 2, a long position in an ITM call option with the strike price K 2, and a short position in an OTM call option with the strike price K 1. The trader's outlook is neutral. This is a capital gain strategy. 31 We have (assuming K 1 ≥ K 2 + D):

T

$$ = $$ ( *K 1 − S T) + − ( *K 2 − S T) + + ( *S T − K 2 ) + − ( *S T − K 1 ) + − D $$ = $$ *K 1 − K 2 − D (236) *max $$ = $$ ( *K 1 − K 2 ) − D (237)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.52. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long box | -0.2% | -11.4% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 68, assignments 18, fees USD 176.80, missing-bar days 53, mark gaps 104. Return at half-spreads 0 / 0.05 / 0.10: 0.4% / -1.0% / -2.4%.

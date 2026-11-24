# 2.11 Short synthetic forward

- Section: 2.11
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*1.0000; short 1 x n call contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy amounts to buying an ATM put option and selling an ATM call option with a strike price K = S 0. This can be a net debit or net credit trade. Typically, *\| H \| ≪ S 0. The trader's outlook is bearish: this strategy mimics a short stock or futures position; it replicates a short forward contract with the delivery price K and the same maturity as the options. This is a capital gain strategy. We have:

fT = (K −ST)+ −(ST −K)+ −H = K −ST −H (37) *S ∗ = K − H (38) *P max = K − H (39) *L max = unlimited (40)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.11. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short synthetic forward | -27.6% | -48.2% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 34, assignments 25, fees USD 88.40, missing-bar days 4, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: -27.3% / -28.0% / -28.6%.

# 2.45 "Short" iron butterfly

- Section: 2.45
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n put contracts at spot*0.9750; long 1 x n put contracts at spot*1.0000; long 1 x n call contracts at spot*1.0000; short 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This volatility strategy is a combination of a bear put spread and a bull call spread and consists of a short position in an OTM put option with a strike price K 1, a long position in an ATM put option and an ATM call option with a strike price *K 2, and a short position in an OTM call option with a strike price K 3. The strikes are equidistant: K 2 − K 1 = K 3 − K 2 = κ. This is a net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (K2 −ST)+ + (ST −K2)+ −(K1 −ST)+ −(ST −K3)+ −D (201) $$ S∗up = K2 + D (202) *S ∗ down = K 2 − D (203) Pmax = \kappa −D (204) *L max = D (205)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.45. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| "short" iron butterfly | -12.5% | -17.3% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 52, assignments 18, fees USD 176.80, missing-bar days 24, mark gaps 5. Return at half-spreads 0 / 0.05 / 0.10: -12.0% / -13.3% / -14.7%.

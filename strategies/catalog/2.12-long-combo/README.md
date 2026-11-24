# 2.12 Long combo

- Section: 2.12
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0250; short 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy (a.k.a. "long risk reversal") amounts to buying an OTM call option with a strike price K 1 and selling an OTM put option with a strike price K 2. The

trader's outlook is bullish. This is a capital gain strategy. 17 We have ( *K 1 \> K 2 ):

$$ fT = (ST −K1)+ −(K2 −ST)+ −H $$ (41) S∗= K1 + H, H > 0 (42) S∗= K2 + H, H < 0 (43) $$ K2 \leqS∗\leqK1, $$ $$ H = 0 $$ (44) *P max = unlimited (45) Lmax = K2 + H (46)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.12. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long combo | 18.4% | -14.5% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 18, assignments 5, fees USD 88.40, missing-bar days 20, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: 18.7% / 18.0% / 17.3%.

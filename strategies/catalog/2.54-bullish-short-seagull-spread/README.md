# 2.54 Bullish short seagull spread

- Section: 2.54
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n put contracts at spot*0.9750; long 1 x n call contracts at spot*1.0000; short 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This option trading strategy is a bull call spread financed with a sale of an OTM put option. It amounts to a short position in an OTM put option with a strike price K 1, a long position in an ATM call option with a strike price K 2, and a short position in an OTM call option with a strike price K 3. Ideally, the trade should be structured to have zero cost. The trader's outlook is bullish. This is a capital gain

$$ fT = −(K1 −ST)+ + (ST −K2)+ −(ST −K3)+ −H $$ (242) S∗= K2 + H, H > 0 (243) S∗= K1 + H, H < 0 (244) $$ K1 \leqS∗\leqK2, $$ $$ H = 0 $$ (245) Pmax = K3 −K2 −H (246) Lmax = K1 + H (247)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.54. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bullish short seagull spread | 8.7% | -15.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 43, assignments 18, fees USD 132.60, missing-bar days 22, mark gaps 4. Return at half-spreads 0 / 0.05 / 0.10: 9.1% / 8.1% / 7.1%.

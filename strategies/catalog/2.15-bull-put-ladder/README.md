# 2.15 Bull put ladder

- Section: 2.15
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n put contracts at spot*1.0000; long 1 x n put contracts at spot*0.9750; long 1 x n put contracts at spot*0.9500. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a vertical spread consisting of a short position in (usually) a close to ATM put option with a strike price K 1, a long position in an OTM put option with a strike price K 2, and a long position in another OTM put option with a lower strike price *K 3. A bull put ladder typically arises when a bull put spread (a bullish strategy) goes wrong (the stock trades lower), so the trader buys another OTM put option (with the strike price K 3 ) to adjust the position to bearish. We have: 19

$$ fT = (K3 −ST)+ + (K2 −ST)+ −(K1 −ST)+ −H $$ (58) S∗up = K1 + H, H < 0 (59) S∗down = K3 + K2 −K1 −H (60) Pmax = K3 + K2 −K1 −H (61) Lmax = K1 −K2 + H (62)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.15. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| bull put ladder | 0.7% | -11.7% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 18, assignments 9, fees USD 132.60, missing-bar days 5, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: 1.2% / 0.1% / -0.9%.

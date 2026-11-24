# 2.21 Diagonal put spread

- Section: 2.21
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*1.1000 (next-next expiry, closed at the near expiry); short 1 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-10-16), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a diagonal spread consisting of a long position in a deep ITM put option with a strike price K 1 and TTM T ′, and a short position in an OTM put option with a strike price K 2 and shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is bearish. At t = T let V be the value of the long put option (expiring at *t = T ′) assuming S T = K. We have:

*P max = V − D (79) *L max = D (80)

If at the expiration of the short put option the stock price K 2 ≤ S T ≤ S stop − loss, where S stop − loss is the stop-loss price above which the trader would unwind the entire position, then the trader can write another OTM put option with TTM T 1 \< T ′. While maintaining the long position in the put option with TTM T ′, the trader can generate income by periodically selling OTM put options with shorter maturities. In this regard, this strategy is similar to the calendar put spread. The main difference is that, in the diagonal put spread the deep ITM put option (unlike the close to

ATM put option in the calendar put spread) more closely mimics the underlying stock, so the position is more protected against a sharp drop in the stock price.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.21. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-10-16, 33 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned. The far leg is closed at the near expiry, so the last monthly expiry is dropped (one cycle fewer).

| | Total return | Max drawdown |
|---|---|---|
| diagonal put spread | 3.8% | -23.7% |
| SPY buy and hold | 56.2% | -18.5% |

Opened 23/33 cycles, ITM leg expiries 4, assignments 4, fees USD 89.70, missing-bar days 339, mark gaps 178. Return at half-spreads 0 / 0.05 / 0.10: 4.0% / 3.3% / 2.6%.

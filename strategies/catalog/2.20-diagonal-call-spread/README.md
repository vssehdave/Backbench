# 2.20 Diagonal call spread

- Section: 2.20
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*0.9000 (next-next expiry, closed at the near expiry); short 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-10-16), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a diagonal spread consisting of a long position in a deep ITM call option with a strike price K 1 and TTM T ′, and a short position in an OTM call option with a strike price K 2 and shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is bullish. At t = T let V be the value of the long call option (expiring at *t = T ′) assuming S T = K. We have:

*P max = V − D (77) *L max = D (78)

If at the expiration of the short call option the stock price S stop − loss ≤ S T ≤ K 2, where S stop − loss is the stop-loss price below which the trader would unwind the entire position, then the trader can write another OTM call option with TTM T 1 \< T ′. While maintaining the long position in the call option with TTM T ′, the trader can generate income by periodically selling OTM call options with shorter maturities. In this regard, this strategy is similar to the calendar call spread. The main difference is that, in the diagonal call spread the deep ITM call option (unlike the close to ATM call option in the calendar call spread) more closely mimics the underlying stock, so the position is more protected against a sharp rise in the stock price.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.20. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-10-16, 33 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned. The far leg is closed at the near expiry, so the last monthly expiry is dropped (one cycle fewer).

| | Total return | Max drawdown |
|---|---|---|
| diagonal call spread | 10.7% | -21.0% |
| SPY buy and hold | 56.2% | -18.5% |

Opened 26/33 cycles, ITM leg expiries 12, assignments 12, fees USD 101.40, missing-bar days 226, mark gaps 144. Return at half-spreads 0 / 0.05 / 0.10: 11.1% / 10.3% / 9.5%.

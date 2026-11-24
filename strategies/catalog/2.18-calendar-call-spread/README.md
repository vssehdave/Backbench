# 2.18 Calendar call spread

- Section: 2.18
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*1.0000 (next-next expiry, closed at the near expiry); short 1 x n call contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-10-16), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a horizontal spread consisting of a long position in a close to ATM call option with TTM T ′ and a short position in another call option with the same strike price *K but shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is neutral to bullish. At the expiration of the short call option ( *t = T), the best case scenario is if the stock price is right at the strike price ( *S T = K). At t = T let V be the value of the long call option (expiring at t = T ′) assuming S T = K. We have: 21

*P max = V − D (73) *L max = D (74)

If at the expiration of the short call option the stock price S stop − loss ≤ S T ≤ K, where S stop − loss is the stop-loss price below which the trader would unwind the entire position, then the trader can write another call option with the strike price *K and TTM T 1 \< T ′. While maintaining the long position in the call option with TTM T ′, the trader can generate income by periodically selling call options with shorter maturities. In this regard, this strategy resembles the covered call strategy.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.18. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-10-16, 33 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned. The far leg is closed at the near expiry, so the last monthly expiry is dropped (one cycle fewer).

| | Total return | Max drawdown |
|---|---|---|
| calendar call spread | -9.1% | -22.9% |
| SPY buy and hold | 56.2% | -18.5% |

Opened 32/33 cycles, ITM leg expiries 24, assignments 24, fees USD 124.80, missing-bar days 103, mark gaps 18. Return at half-spreads 0 / 0.05 / 0.10: -8.7% / -9.7% / -10.6%.

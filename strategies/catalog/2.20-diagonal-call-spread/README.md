# 2.20 Diagonal call spread

- Section: 2.20
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a diagonal spread consisting of a long position in a deep ITM call option with a strike price K 1 and TTM T ′, and a short position in an OTM call option with a strike price K 2 and shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is bullish. At t = T let V be the value of the long call option (expiring at *t = T ′) assuming S T = K. We have:

*P max = V − D (77) *L max = D (78)

If at the expiration of the short call option the stock price S stop − loss ≤ S T ≤ K 2, where S stop − loss is the stop-loss price below which the trader would unwind the entire position, then the trader can write another OTM call option with TTM T 1 \< T ′. While maintaining the long position in the call option with TTM T ′, the trader can generate income by periodically selling OTM call options with shorter maturities. In this regard, this strategy is similar to the calendar call spread. The main difference is that, in the diagonal call spread the deep ITM call option (unlike the close to ATM call option in the calendar call spread) more closely mimics the underlying stock, so the position is more protected against a sharp rise in the stock price.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.20. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

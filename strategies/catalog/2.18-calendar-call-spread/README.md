# 2.18 Calendar call spread

- Section: 2.18
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a horizontal spread consisting of a long position in a close to ATM call option with TTM T ′ and a short position in another call option with the same strike price *K but shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is neutral to bullish. At the expiration of the short call option ( *t = T), the best case scenario is if the stock price is right at the strike price ( *S T = K). At t = T let V be the value of the long call option (expiring at t = T ′) assuming S T = K. We have: 21

*P max = V − D (73) *L max = D (74)

If at the expiration of the short call option the stock price S stop − loss ≤ S T ≤ K, where S stop − loss is the stop-loss price below which the trader would unwind the entire position, then the trader can write another call option with the strike price *K and TTM T 1 \< T ′. While maintaining the long position in the call option with TTM T ′, the trader can generate income by periodically selling call options with shorter maturities. In this regard, this strategy resembles the covered call strategy.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.18. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

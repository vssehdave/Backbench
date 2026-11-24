# 2.19 Calendar put spread

- Section: 2.19
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a horizontal spread consisting of a long position in a close to ATM put option with TTM T ′ and a short position in another put option with the same strike price *K but shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is neutral to bearish. At the expiration of the short put option ( *t = T), the best case scenario is if the stock price is right at the strike price ( *S T = K). At t = T let V be the value of the long put option (expiring at t = T ′) assuming S T = K. We have:

*P max = V − D (75) *L max = D (76)

If at the expiration of the short put option the stock price K ≤ S T ≤ S stop − loss, where S stop − loss is the stop-loss price above which the trader would unwind the

entire position, then the trader can write another put option with the strike price *K and TTM T 1 \< T ′. While maintaining the long position in the put option with TTM T ′, the trader can generate income by periodically selling put options with shorter maturities. In this regard, this strategy resembles the covered put strategy.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.19. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

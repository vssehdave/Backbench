# 2.21 Diagonal put spread

- Section: 2.21
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a diagonal spread consisting of a long position in a deep ITM put option with a strike price K 1 and TTM T ′, and a short position in an OTM put option with a strike price K 2 and shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is bearish. At t = T let V be the value of the long put option (expiring at *t = T ′) assuming S T = K. We have:

*P max = V − D (79) *L max = D (80)

If at the expiration of the short put option the stock price K 2 ≤ S T ≤ S stop − loss, where S stop − loss is the stop-loss price above which the trader would unwind the entire position, then the trader can write another OTM put option with TTM T 1 \< T ′. While maintaining the long position in the put option with TTM T ′, the trader can generate income by periodically selling OTM put options with shorter maturities. In this regard, this strategy is similar to the calendar put spread. The main difference is that, in the diagonal put spread the deep ITM put option (unlike the close to

ATM put option in the calendar put spread) more closely mimics the underlying stock, so the position is more protected against a sharp drop in the stock price.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.21. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

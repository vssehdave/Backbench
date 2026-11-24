# 2.15 Bull put ladder

- Section: 2.15
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a short position in (usually) a close to ATM put option with a strike price K 1, a long position in an OTM put option with a strike price K 2, and a long position in another OTM put option with a lower strike price *K 3. A bull put ladder typically arises when a bull put spread (a bullish strategy) goes wrong (the stock trades lower), so the trader buys another OTM put option (with the strike price K 3 ) to adjust the position to bearish. We have: 19

$$ fT = (K3 −ST)+ + (K2 −ST)+ −(K1 −ST)+ −H $$ (58) S∗up = K1 + H, H < 0 (59) S∗down = K3 + K2 −K1 −H (60) Pmax = K3 + K2 −K1 −H (61) Lmax = K1 −K2 + H (62)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.15. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

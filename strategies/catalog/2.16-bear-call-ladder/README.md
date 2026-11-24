# 2.16 Bear call ladder

- Section: 2.16
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a short position in (usually) a close to ATM call option with a strike price K 1, a long position in an OTM call option with a strike price K 2, and a long position in another OTM call option with a higher strike price *K 3. A bear call ladder typically arises when a bear call spread (a bearish strategy) goes wrong (the stock trades higher), so the trader buys another OTM call option (with the strike price K 3 ) to adjust the position to bullish. We have:

$$ fT = (ST −K3)+ + (ST −K2)+ −(ST −K1)+ −H $$ (63) *S ∗ down = K 1 − H, H < 0 (64) $$ S∗up = K3 + K2 −K1 + H $$ (65) *P max = unlimited (66) Lmax = K2 −K1 + H (67)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.16. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

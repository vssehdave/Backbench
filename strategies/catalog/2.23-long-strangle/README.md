# 2.23 Long strangle

- Section: 2.23
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a long position in an OTM call option with a strike price K 1, and a long position in an OTM put option with a strike price K 2. This is a net debit trade. However, because both call and put options are OTM, this strategy is less costly to establish than a long straddle position. The flipside is that the movement in the stock price required to reach one of the break-even points is also more significant. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (ST −K1)+ + (K2 −ST)+ −D $$ (86) S∗up = K1 + D (87) *S ∗ down = K 2 − D (88) *P max = unlimited (89) *L max = D (90)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.23. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

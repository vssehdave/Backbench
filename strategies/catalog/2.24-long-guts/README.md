# 2.24 Long guts

- Section: 2.24
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a long position in an ITM call option with a strike price K 1, and a long position in an ITM put option with a strike price K 2. This is a net debit trade. Since both call and put options are ITM, this strategy

is more costly to establish than a long straddle position. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming D \> K 2 − K 1 ): 23

$$ fT = (ST −K1)+ + (K2 −ST)+ −D $$ (91) S∗up = K1 + D (92) *S ∗ down = K 2 − D (93) *P max = unlimited (94) Lmax = D −(K2 −K1) (95)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.24. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

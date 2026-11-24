# 2.27 Short guts

- Section: 2.27
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a sideways strategy consisting of a short position in an ITM call option with a strike price K 1, and a short position in an ITM put option with a strike price *K 2. This is a net credit trade. Since both call and put options are ITM, the initial

credit is higher than in a short straddle position. The flipside is that the risk is also higher. The trader's outlook is neutral. This is an income strategy. We have: 24

$$ fT = −(ST −K1)+ −(K2 −ST)+ + C $$ (106) S∗up = K1 + C (107) *S ∗ down = K 2 − C (108) Pmax = C −(K2 −K1) (109) *L max = unlimited (110)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.27. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

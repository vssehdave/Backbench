# 2.26 Short strangle

- Section: 2.26
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a sideways strategy consisting of a short position in an OTM call option with a strike price K 1, and a short position in an OTM put option with a strike price K 2. This is a net credit trade. Since both call and put options are OTM, this strategy is less risky than a short straddle position. The flipside is that the initial credit is also lower. The trader's outlook is neutral. This is an income strategy. We have:

$$ fT = −(ST −K1)+ −(K2 −ST)+ + C $$ (101) S∗up = K1 + C (102) *S ∗ down = K 2 − C (103) *P max = C (104) *L max = unlimited (105)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.26. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

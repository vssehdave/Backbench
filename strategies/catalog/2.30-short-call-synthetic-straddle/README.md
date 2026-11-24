# 2.30 Short call synthetic straddle

- Section: 2.30
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This sideways strategy (which is the same as a short straddle with the put replaced by a synthetic put) amounts to buying stock and selling two ATM (or the nearest

OTM) call options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming S 0 ≤ K):

$$ fT = ST −S0 −2 \times (ST −K)+ + C $$ (121) S∗up = 2 \times K −S0 + C (122) *S ∗ down = S 0 − C (123) Pmax = K −S0 + C (124) *L max = unlimited (125)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.30. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

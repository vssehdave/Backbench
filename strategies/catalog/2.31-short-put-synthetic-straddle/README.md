# 2.31 Short put synthetic straddle

- Section: 2.31
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This sideways strategy (which is the same as a short straddle with the call replaced by a synthetic call) amounts to shorting stock and selling two ATM (or the nearest OTM) put options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming S 0 ≥ K):

$$ fT = S0 −ST −2 \times (K −ST)+ + C $$ (126) S∗up = S0 + C (127) S∗down = 2 \times K −S0 −C (128) Pmax = S0 −K + C (129) *L max = unlimited (130)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.31. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

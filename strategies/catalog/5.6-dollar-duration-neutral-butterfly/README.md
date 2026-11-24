# 5.6 Dollar-duration-neutral butterfly

- Section: 5.6
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

This is a zero-cost combination of a long barbell portfolio (with short T 1 and long *T 3 maturities) and a short bullet portfolio (with a medium maturity T 2, where *T 1 \< T 2 \< T 3 ). Let: the dollar amounts invested in the 3 bonds be P 1 , P 2 , P 3; and

91 For the sake of simplicity, in Eq. (396) the number n = T ∗ /δ of compounding periods is assumed to be a whole number. Extension to non-integer T ∗ /δ is straightforward.

the corresponding modified durations be D 1 , D 2 , D 3. Then zero cost (i.e., dollarneutrality) and the dollar-duration-neutrality (the latter protects the portfolio from parallel shifts in the yield curve) imply that

P1 + P3 = P2 (404) $$ P1 D1 + P3 D3 = P2 D2 $$ (405)

This fixes P 1 , P 3 via P 2. While the portfolio is immune to parallel shifts in the yield curve, it is not immune to changes in the slope or the curvature of the yield curve. 93

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

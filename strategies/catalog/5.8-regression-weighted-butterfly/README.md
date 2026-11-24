# 5.8 Regression-weighted butterfly

- Section: 5.8
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

Empirically, short-term interest rates are sizably more volatile than long-term interest rates. 94 Therefore, the interest rate spread change between the body and the short-maturity wing (of the butterfly - see above) can be expected to be greater by some factor - call it β - than the spread change between the long-maturity wing and the body (so, typically β \> 1). This factor can be obtained from historical data via, e.g., running a regression of the spread change between the body and the short-maturity wing over the spread change between the long-maturity wing and the body. Then, instead of Eq. (406), we have the following dollar-duration-neutrality and "curve-neutrality" conditions:

P1 D1 + P3 D3 = P2 D2 (407) $$ P1 D1 = \beta P3 D3 $$ (408)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.8. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

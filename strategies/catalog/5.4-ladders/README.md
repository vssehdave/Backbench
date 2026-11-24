# 5.4 Ladders

- Section: 5.4
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

A ladder is a bond portfolio with (roughly) equal capital allocations into bonds of n different maturities T i, i = 1 ,..., n (where the number of rungs n is sizable, e.g., n = 10). The maturities are equidistant: T i +1 = T i + δ. This is a durationtargeting strategy, 89 which maintains an approximately constant duration by selling shorter-maturity bonds as they approach maturity and replacing them with new longer-maturity bonds. A ladder portfolio aims to diversify the interest rate and reinvestment risks 90 by avoiding exposure to only a few maturities (as in bullets and barbells). It also generates a regular revenue stream from the coupons of each bond. The maturity of a ladder portfolio can be defined as the average maturity:

T = 1 *n n X $$ i=1 $$ *i (395)

The income is higher for higher values of T; however, so is the interest rate risk.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# 5.7 Fifty-fifty butterfly

- Section: 5.7
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

This is a variation of the standard butterfly. In the above notations for the dollarduration-neutral butterfly, we have

P1 D1 = P3 D3 = 1

2 P 2 D 2 (406)

So, the fifty-fifty butterfly is still dollar-duration-neutral, but it is no longer dollarneutral (i.e., it is not a zero-cost strategy). Instead, dollar durations of the wings are the same (hence the term "fifty-fifty"). As a result, the strategy is (approximately) neutral to small steepening and flattening of the yield curve, to wit, if the interest rate spread change between the body and the short-maturity wing is equal to the spread change between the long-maturity wing and the body. That is why this strategy is a.k.a. "neutral curve butterfly" (whose cost is non-dollar-neutrality).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

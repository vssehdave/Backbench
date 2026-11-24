# 5.13 Yield curve spread (flatteners & steepeners)

- Section: 5.13
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

This strategy consists of buying or selling the yield curve spread. 101 The yield curve spread is defined as the difference between the yields of two bonds of the same issuer with different maturities. If the interest rates are expected to fall, the yield curve is expected to steepen. If the interest rates are expected to rise, the yield curve is expected to flatten. The yield curve spread strategy can be summarized via the following rule: Rule = (

Flattener: Short spread if interest rates are expected to rise Steepener: Buy spread if interest rates are expected to fall (416)

Shorting the spread amounts to selling shorter-maturity bonds (a.k.a. the front leg) and buying longer-maturity bonds (a.k.a. the back leg). Buying the spread is the opposite trade: buying the front leg and selling the back leg. If the yield curve has parallel shifts, this strategy can generate losses. Matching dollar durations of the front and back legs immunizes the portfolio to small parallel shifts in the yield curve.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.13. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

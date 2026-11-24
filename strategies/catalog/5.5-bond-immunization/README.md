# 5.5 Bond immunization

- Section: 5.5
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

Bond immunization is used in cases such as a predetermined future cash obligation. A simple solution would be to purchase a zero-coupon bond with the required maturity (and desirable/acceptable yield). However, such a bond may not always be available in the market, so a portfolio of bonds with varying maturities must be used instead. Such a portfolio is subject to the interest rate and reinvestment risks. One way to mitigate these risks is to build a portfolio whose duration matches the maturity of the future cash obligation (thereby "immunizing" the bond portfolio against parallel shifts in the yield curve). Consider a portfolio of bonds with 2 different maturities T 1 , T 2 and the corresponding durations D 1 , D 2 (where "duration" means modified duration). Let: the dollar amounts invested in these bonds be P 1 , P 2; the total amount to be invested be P; the desired duration of the portfolio be D (which

is related to the maturity T ∗ of the future cash obligation - see below); and the *constant yield (which is assumed to be the same for all bonds - see below) be Y. Then P is fixed using Y and the amount of the future obligation F: $$ P = F/(1 + Y \delta)T∗/\delta $$ (396)

where we are assuming periodic compounding and δ is the length of each compounding period (e.g., 1 year). 91 Then we have:

P1 + P2 = P (397) $$ P1 D1 + P2 D2 = P D $$ (398) where $$ D = T∗/(1 + Y \delta) $$ (399)

With 3 bonds, we can also match the convexity:

P1 + P2 + P3 = P

(400) $$ P1 D1 + P2 D2 + P3 D3 = P D $$ (401) $$ P1 C1 + P2 C2 + P3 C3 = P C $$ (402)

where C 1 , C 2 , C 3 are the convexities of the 3 bonds and

$$ C = T∗(T∗+ \delta)/(1 + Y \delta)2 $$ (403)

In practice, the yield curve changes over time, which (among other things) requires that the portfolio be periodically rebalanced. This introduces nontrivial transaction costs, which must also be accounted for. Furthermore, the yields are not the same for all bonds in the portfolio, which introduces additional complexity into the problem. 92

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

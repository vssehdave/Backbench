# 3.9 Mean-reversion - single cluster

- Section: 3.9
- Asset class: Stocks
- Harness status: **not testable: cross-sectional universe** - cross-sectional mean reversion by cluster; needs a stock universe and short selling.

## Description (paper)

This is a generalization of the pairs trading strategy to N \> 2 stocks that are historically highly correlated (e.g., stocks belonging to the same industry or sector). Let R i, i = 1 ,..., N, be the returns for these N stocks: *R i = ln  *P i ( *t 2 ) *P i ( *t 1 )  (292)

R = 1

N

N X $$ i=1 $$ *i (293) e *R i = R i − R (294)

Following the pairs trading intuition, we can short stocks with positive e *R i and buy stocks with negative e *R i. We have the following conditions:

N X $$ i=1 $$ *P i \| Q i \| = I (295)

N X $$ i=1 $$ Pi Qi = 0 (296)

Here: I is the total desired dollar investment; Eq. (296) is the dollar-neutrality constraint; Q i \< 0 for short-sales; Q i \> 0 for buys; P i are the prices at the time the position is established. We have 2 equations and N \> 2 unknowns. A simple prescription (which is one out of myriad possibilities) for specifying Q i is to have the dollar positions D i = P i Q i proportional to the demeaned returns: Di = −\gamma eRi (297)

where γ \> 0 (recall that we short e *R i \> 0 stocks and buy e *R i \< 0 stocks). Then Eq. (296) is automatically satisfied, while Eq. (295) fixes γ: $$ \gamma = $$ *I N $$ i=1 $$ e *R i (298)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.9. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

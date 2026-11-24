# 3.8 Pairs trading

- Section: 3.8
- Asset class: Stocks
- Harness status: **not testable: multiple instruments** - trades a pair of stocks long/short; needs two series and short selling.

## Description (paper)

*i, and shorting stocks in the bottom decile (with (non)uniform weights).

3.8

This dollar-neutral strategy amounts to identifying a pair of historically highly correlated stocks (call them stock A and stock B) and, when a mispricing (i.e., a deviation from the high historical correlation) occurs, shorting the "rich" stock and buying the "cheap" stock. This is an example of a mean-reversion strategy. Let P A ( *t 1 ) and *P B ( *t 1 ) be the prices of stock A and stock B at time t 1, and let P A ( *t 2 ) and P B ( *t 2 ) be the prices of stock A and stock B at a later time t 2. All prices are fully adjusted for any splits and dividends. The corresponding returns (from t 1 to t 2 ) are

RA = PA(t2) *P A ( *t 1 ) − 1 (283)

RB = PB(t2) *P B ( *t 1 ) − 1 (284)

Since typically these returns are small, we can use an alternative definition: *R A = ln  *P A ( *t 2 ) *P A ( *t 1 )  (285) *R B = ln  *P B ( *t 2 ) *P B ( *t 1 )  (286)

Next, let e *R A and e *R B be the demeaned returns:

R = 1

2 ( R A + R B ) (287)

e R A = R A − R (288) e *R B = R B − R (289)

where R is the mean return. A stock is "rich" if its demeaned return is positive, and it is "cheap" if its demeaned return is negative. The numbers of shares Q A, Q B to short/buy are fixed by the total desired dollar investment I (Eq. (290)) and the requirement of dollar-neutrality (Eq. (291)):

P A \| Q A \| + P B \| Q B \| = I (290) PA QA + PB QB = 0 (291)

where P A, P B are the stock prices at the time t ∗ the position is established ( *t ∗ ≥ t 2 ). 52

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.8. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

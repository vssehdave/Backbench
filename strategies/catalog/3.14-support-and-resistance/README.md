# 3.14 Support and resistance

- Section: 3.14
- Asset class: Stocks
- Harness status: **not testable: needs high/low/volume** - pivot point uses the previous high and low; decide() receives closes only.

## Description (paper)

This strategy uses "support" S and "resistance" R levels, which can be computed using the "pivot point" (a.k.a. the "center") C as follows: 56

C = PH + PL + PC (325)

R = 2 \times C −PL (326) S = 2 \times C −PH (327)

Here P H, P L and P C are the previous day's high, low and closing prices. One way to define a trading signal is as follows (as above, P is the current price): Signal =         

Establish long position if P \> C Liquidate long position if P ≥ R Establish short position if P \< C Liquidate short position if P ≤ S (328)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.14. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

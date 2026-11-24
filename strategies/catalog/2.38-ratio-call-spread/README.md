# 2.38 Ratio call spread

- Section: 2.38
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy consists of a short position in N S close to ATM call options with a strike price K 1, and a long position in N L ITM call options with a strike price K 2, where N L \< N S. Typically, N L = 1 and N S = 2, or N L = 2 and N S = 3. This is an income strategy if it is structured as a net credit trade. The trader's outlook is neutral to bearish. We have: 28

fT = NL × (ST −K2)+ −NS × (ST −K1)+ −H (158) S∗down = K2 + H/NL, H > 0 (159) S∗up = (NS \times K1 −NL \times K2 −H)/(NS −NL) (160) Pmax = NL × (K1 −K2) −H (161) *L max = unlimited (162)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.38. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# 2.39 Ratio put spread

- Section: 2.39
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy consists of a short position in N S close to ATM put options with a strike price K 1, and a long position in N L ITM put options with a strike price K 2, where N L \< N S. Typically, N L = 1 and N S = 2, or N L = 2 and N S = 3. This is an income strategy if it is structured as a net credit trade. The trader's outlook is neutral to bullish. We have:

fT = NL × (K2 −ST)+ −NS × (K1 −ST)+ −H (163) *S ∗ up = K 2 − H/N L , H > 0 (164) S∗down = (NS \times K1 −NL \times K2 + H)/(NS −NL) (165) Pmax = NL × (K2 −K1) −H (166) Lmax = NS \times K1 −NL \times K2 + H (167)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.39. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

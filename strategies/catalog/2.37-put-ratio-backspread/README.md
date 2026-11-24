# 2.37 Put ratio backspread

- Section: 2.37
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy consists of a short position in N S close to ATM put options with a strike price K 1, and a long position in N L OTM put options with a strike price K 2, where N L \> N S. Typically, N L = 2 and N S = 1, or N L = 3 and N S = 2. The trader's outlook is strongly bearish. This is a capital gain strategy. We have:

fT = NL × (K2 −ST)+ −NS × (K1 −ST)+ −H (153) S∗up = K1 + H/NS, H < 0 (154) S∗down = (NL \times K2 −NS \times K1 −H)/(NL −NS) (155) Pmax = NL \times K2 −NS \times K1 −H (156) $$ Lmax = NS \times (K1 −K2) + H $$ (157)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.37. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# 2.36 Call ratio backspread

- Section: 2.36
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy consists of a short position in N S close to ATM call options with a strike price K 1, and a long position in N L OTM call options with a strike price K 2, where N L \> N S. Typically, N L = 2 and N S = 1, or N L = 3 and N S = 2. The trader's outlook is strongly bullish. This is a capital gain strategy. We have: 27

fT = NL × (ST −K2)+ −NS × (ST −K1)+ −H (148) *S ∗ down = K 1 − H/N S , H < 0 (149) S∗up = (NL \times K2 −NS \times K1 + H)/(NL −NS) (150) *P max = unlimited (151) $$ Lmax = NS \times (K2 −K1) + H $$ (152)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.36. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

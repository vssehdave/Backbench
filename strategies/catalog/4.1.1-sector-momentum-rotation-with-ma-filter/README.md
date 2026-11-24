# 4.1.1 Sector momentum rotation with MA filter

- Section: 4.1.1
- Asset class: Exchange-traded funds
- Harness status: **not testable: cross-sectional universe** - sector ETF rotation with an MA filter; needs several ETF series at once.

## Description (paper)

This is a variation/refinement of the sector momentum rotation strategy. An ETF in the top (bottom) decile is bought (sold) only if it passes an additional filter based on a moving average MA( *T ′) of this ETF's price: Rule = (

Buy top-decile ETFs only if P \> MA( *T ′) Short bottom-decile ETFs only if P \< MA( *T ′) (362)

Here P is the ETF's price at the time of the transaction, and MA( *T ′) is computed using daily prices ( *T ′ can but need not be equal T; e.g., T ′ can be 100 to 200 days).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

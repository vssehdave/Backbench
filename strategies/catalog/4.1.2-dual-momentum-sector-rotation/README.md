# 4.1.2 Dual-momentum sector rotation

- Section: 4.1.2
- Asset class: Exchange-traded funds
- Harness status: **not testable: cross-sectional universe** - dual-momentum rotation among several ETFs and a safe asset; needs several series at once.

## Description (paper)

In long-only strategies, to mitigate the risk of buying ETFs when the broad market is trending down, relative (i.e., cross-sectional) momentum of sector ETFs can be augmented by the absolute (i.e., time-series) momentum of, e.g., a broad market index ETF (see, e.g., \[Antonacci, 2014\], \[Antonacci, 2017\]). 76 So, a long position based on the sector rotation signal (discussed above) is established only if the broad

market index has an upward trend; otherwise, the total available funds are invested into an ETF (e.g., gold or Treasury ETF) uncorrelated with the broad market index: Rule = (

Buy top-decile ETFs if P \> MA( *T ′) Buy an uncorrelated ETF if P ≤ MA( *T ′) (363)

Here P is the broad market index ETF's price at the time of the transaction, and MA( *T ′) is the moving average of this ETF's price. Typically, T ′ is 100 to 200 days.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

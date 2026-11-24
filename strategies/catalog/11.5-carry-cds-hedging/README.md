# 11.5 Carry - CDS hedging

- Section: 11.5
- Asset class: Structured assets
- Harness status: **not testable: bonds/rates** - needs credit tranche, CDS or MBS data.

## Description (paper)

This strategy amounts to buying a low quality tranche and Delta-hedging the position by selling a single-name CDS with lower premium payments than the long tranche (instead of the index or a higher quality tranche). The hedge ratio is given by Eq. (487) with D ix replaced by the risky duration D CDS of the CDS:

∆ CDS = *D CDS (489)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 11.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

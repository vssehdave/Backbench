# 11.4 Carry - tranche hedging

- Section: 11.4
- Asset class: Structured assets
- Harness status: **not testable: bonds/rates** - needs credit tranche, CDS or MBS data.

## Description (paper)

This strategy amounts to selling a high quality tranche (e.g., senior/mezzanine) and Delta-hedging the position by buying the index. 179 The Delta is given by Eq. (487).

11.4

This strategy amounts to buying a low quality tranche and Delta-hedging the position by selling a high quality tranche. The hedge ratio is given by: ∆ *high = D low high (488)

Here D low and D high are the risky durations of the low and high quality tranches.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 11.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

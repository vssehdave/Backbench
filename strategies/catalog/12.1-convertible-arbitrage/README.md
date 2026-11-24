# 12.1 Convertible arbitrage

- Section: 12.1
- Asset class: Convertibles
- Harness status: **not testable: options chains** - needs convertible bond and embedded-option data.

## Description (paper)

A convertible bond is a hybrid security with an embedded option to convert the bond

(a fixed-income instrument) to a preset number (knows as the conversion ratio) of the issuer's stock (an equity instrument) when, e.g., the stock price reaches a preset level (known as the conversion price). Empirically, convertibles at the issuance tend to be undervalued relative to their "fair" value. 184 This gives rise to arbitrage opportunities. A convertible arbitrage strategy amounts to buying a convertible bond and simultaneously shorting h units of the underlying stock, where the hedge ratio is given by

h = ∆\\times C (492) $$ ∆= \partialV/\partialS $$ (493)

Here: C is the conversion ratio; V is the value of the conversion option (which is

model-dependent); S is the underlying stock price; and ∆is the (model-dependent)

Delta of the conversion option. 185 Typically, the position is held for 6-12 months starting at the issuance date of the convertible and the hedge ratio is updated daily.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 12.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

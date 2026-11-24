# 5.8.1 Maturity-weighted butterfly

- Section: 5.8.1
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

This is a variation of the regression-weighted butterfly, where instead of fixing β in Eq. (408) via a regression based on historical data, this coefficient is based on the 3 bond maturities: $$ \beta = T2 −T1 $$

T 3 − T 2 (409)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.8.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# 5.14 CDS basis arbitrage

- Section: 5.14
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

A credit default swap (CDS) is insurance against default on a bond. 102 The CDS price, known as the CDS spread, is a periodic (e.g., annual) premium per dollar of the insured debt. The CDS essentially makes the bond a risk-free instrument. Therefore, the CDS spread should equal the bond yield spread, i.e., the spread between the bond yield and the risk-free rate. The difference between the CDS spread and the bond spread is known as the CDS basis: CDS basis = CDS spread − bond spread (417)

Negative basis indicates that the bond spread is too high relative to the CDS spread, i.e., the bond is relatively cheap. The CDS arbitrage trade then amounts to buying the bond and insuring it with the CDS 103 thereby generating a risk-free profit. 104

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.14. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

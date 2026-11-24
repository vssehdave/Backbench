# 9.2 Trading based on hedging pressure

- Section: 9.2
- Asset class: Commodities
- Harness status: **not testable: futures** - needs commodity futures or term-structure data.

## Description (paper)

This strategy is based on hedgers' and speculators' position data provided (weekly) by the U.S. Commodity Futures Trading Commission (CFTC) in the Commitments of Traders (COT) reports. For each commodity, the "hedging pressure" (HP), separately for hedgers and speculators, is calculated as the number of long contracts divided by the total number of contracts (long plus short). So, HP is between 0 and 1. High (low) hedgers' HP is indicative of contango (backwardation), while high (low) speculators' HP is indicative of backwardation (contango). A zero-cost portfolio can be constructed, e.g., as follows. First, the cross-section of commodities is divided into the upper half and the lower half by the speculators' HP. Then, the upper half commodity futures are bought if they are in the bottom quintile by the hedgers' HP, and the lower half commodity futures are sold if they are in the top quintile by the hedger's HP. Typical formation and holding periods are 6 months. 153

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 9.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

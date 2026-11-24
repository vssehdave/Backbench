# 6.4 Intraday arbitrage between index ETFs

- Section: 6.4
- Asset class: Indexes
- Harness status: **not testable: multiple instruments** - intraday arbitrage between two index ETFs; needs intraday data and a short leg.

## Description (paper)

This strategy amounts to exploiting short-term mispricings between two ETFs (call them ETF1 and ETF2) on the same underlying index. 118 It can be summarized as

\times \kappa Liquidate position if P Bid ≥ P Ask Buy ETF1, short ETF2 if P Bid ≥ P Ask*

\times \kappa Liquidate position if P Bid ≥ P Ask (428)

Here: κ is a predefined threshold, which is close to 1, e.g., κ = 1 . 002 (see, e.g., \[Marshall, Nguyen and Visaltanachoti\]); P Bid and P Bid*

are the bid prices for ETF1 and ETF2, and P Ask and P Ask*

are the ask prices. Marketable "fill or kill" limit orders can be used to execute the trades. Such arbitrage opportunities are ephemeral and require a fast order execution system or else slippage will eat away the profits.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 6.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

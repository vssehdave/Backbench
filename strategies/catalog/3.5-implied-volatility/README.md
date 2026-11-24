# 3.5 Implied volatility

- Section: 3.5
- Asset class: Stocks
- Harness status: **not testable: data not available** - Alpaca option bars start 2024-01-18 and carry no implied volatility or bid/ask (docs/options.md); the strategy ranks stocks by IV level or its change across the chain.

## Description (paper)

This strategy is based on the empirical observation that stocks with larger increases in call implied volatilities over the previous month on average have higher future returns, while stocks with larger increases in put implied volatilities over the previous month on average have lower future returns (see, e.g., \[An et al, 2014\], \[Chen, Chung and Tsai, 2016\]). 45 Therefore, the trader can, e.g., construct a dollar-neutral portfolio by buying stocks in the top decile by the increase in call implied volatilities, and shorting stocks in the top decile by the increase in put implied volatilities. One can also consider variations, e.g., buying stocks in the top decile by the difference twixt the change in call implied volatilities and the change in put implied volatilities.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

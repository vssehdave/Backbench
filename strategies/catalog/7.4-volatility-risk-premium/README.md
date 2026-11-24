# 7.4 Volatility risk premium

- Section: 7.4
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

Empirical evidence indicates that implied volatility tends to be higher than realized volatility most of the time, which is known as the "volatility risk premium". 133

Simply put, most of the time options are priced higher than the prices one would expect based on realized volatility, so the idea is to sell volatility. E.g., the trader can sell straddles based on S&P 500 options. As a possible proxy for volatility risk premium, the trader can, e.g., use the difference between VIX at the beginning of the current month and the realized volatility (in %, as VIX is quoted in %) of S&P 500 daily returns since the beginning of the current month. If the spread is positive, the trader sells the straddle. If the volatility spikes (which usually happens if the market sells of), the strategy will lose money. It is profitable in sideways markets. 134

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

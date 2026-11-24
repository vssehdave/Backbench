# 12.2 Convertible option-adjusted spread

- Section: 12.2
- Asset class: Convertibles
- Harness status: **not testable: options chains** - needs convertible bond and embedded-option data.

## Description (paper)

This strategy amounts to simultaneously buying and selling two different convertible bonds of the same issuer. The long position is in a bond with a higher optionadjusted spread (OAS), and the short position is in a bond with a lower OAS (see, e.g., \[Calamos, 2003\]). Then the trade is profitable if these two spreads converge.

The OAS can be calculated as follows (see, e.g., \[Hull, 2012\]). 186 A straightforward (but not the only) 187 way to compute the price P C of the convertible bond is to assume that

PC = PB + V (494)

where P B is the price of the straight bond (without the embedded option), and V is the value of the conversion option, which is a call option. P B is computed via the standard discounting of the future cash flows of the bond. On the other hand, V depends on the risk-free interest rate curve. At the initial iteration, V is computed (using a pricing model for the call option) assuming the zero-coupon government Treasury curve as the risk-free interest rate curve. This initial iteration V (0) may not coincide with P mkt C − P B, where P mkt*

*C is the market price of the convertible bond. Then one iteratively (e.g., using the bisection method) parallel-shifts the input Treasury curve until V computed using the so-shifted curve is such that V = mkt*

*C − P B. The curve parallel shift obtained via this iterative procedure is the OAS.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 12.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

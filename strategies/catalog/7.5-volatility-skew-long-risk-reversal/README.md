# 7.5 Volatility skew - long risk reversal

- Section: 7.5
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

OTM put options with the underlying at S 0 = K + κ tend to be priced higher than OTM call options with the underlying at S 0 = K − κ (here K is the strike price, and κ \> 0 is the distance from the strike). I.e., with all else being equal, the implied volatility for puts is higher than for calls. 136 The long risk reversal strategy (see Subsection 2.12), where the trader buys an OTM call option and sells an OTM put option, captures this skew. However, this is a directional strategy - it loses money if the price of the underlying drops below K put − C, where K put is the strike price of the put, and C \> 0 is the premium of the put minus the premium of the call.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

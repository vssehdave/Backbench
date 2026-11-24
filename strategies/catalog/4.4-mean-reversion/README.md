# 4.4 Mean-reversion

- Section: 4.4
- Asset class: Exchange-traded funds
- Harness status: **not testable: needs high/low/volume** - internal bar strength uses high and low; the strategy is also cross-sectional across ETFs and short.

## Description (paper)

One way (among myriad others) to construct a mean-reversion strategy for ETFs is

to use the Internal Bar Strength (IBS) based on the previous day's close P C, high *P H and low P L prices: 80

IBS = P C − P L

P H − P L

(370)

Note that IBS ranges from 0 to 1. 81 An ETF can be thought of as being "rich" if its

IBS is close to 1, and as "cheap" if its IBS is close to 0. Upon sorting a universe of ETFs cross-sectionally by IBS, a dollar-neutral strategy can, e.g., be constructed by selling ETFs in the top decile and buying ETFs in the bottom decile. As with stock strategies discussed above, weights can be uniform for all long and all short ETFs, respectively, or nonuniform, e.g., based on historical ETF volatilities. Furthermore, mean-reversion strategies we discussed above for stocks can also be adapted to ETFs.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

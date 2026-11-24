# 7.3 Volatility carry with two ETNs

- Section: 7.3
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

VXX is an exchange-traded note (ETN) that tracks VIX via a portfolio of shortmaturity (months 1 and 2) VIX futures contracts. To maintain a constant maturity, at the close of each day, a portion of the shorter-maturity futures is sold and replaced with the longer-maturity futures bought with the proceeds. Since the VIX futures curve is in contango most of the time, the longer-maturity futures are priced higher than the shorter-maturity futures, so this rebalancing amounts to a decay in the value of VXX over time, which is known as the roll (or contango) loss. Further, as time passes, the futures converge to the spot (VIX), so VXX loses value so long as the VIX futures curve is in contango. VXZ is yet another ETN that tracks VIX via a portfolio of medium-maturity (months 4 through 7) VIX futures. VXZ also suffers roll loss, but to a lesser degree than VXX as the slope of the VIX futures curve in contango decreases with maturity. 130 The basic strategy then is to short VXX and buy VXZ with the hedge ratio that can be determined via a serial regression. 131

This strategy is not without risks, however. There can be short-term spikes in VXX (the corresponding spikes in VXZ usually are sizably smaller), which can lead to substantial short-term P&L drawdowns, even if the strategy is overall profitable.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

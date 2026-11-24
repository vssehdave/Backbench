# 3.19 Market-making

- Section: 3.19
- Asset class: Stocks
- Harness status: **not testable: other data not available** - needs order-book or quote data and intraday execution; the harness is daily.

## Description (paper)

Over-simplistically, this strategy amounts to capturing the bid-ask spread for a given stock and can be (again, over-simplistically) summarized as follows: Rule = ( Buy at the bid Sell at the ask (359)

In a market where most order flow is "dumb" (or uninformed), this strategy on average would work very well. However, in a market where most order flow is "smart" (or informed, i.e., "toxic"), this strategy, as stated, would lose money. This is because of adverse selection, where, precisely because most order flow is smart, most fills at the bid (ask) would be when the market is trading through it downward (upward), so these trades would lose money. Furthermore, most limit orders to buy (sell) at the bid (ask) would never be filled as the price would run away from them, i.e., increase (decrease). So, ideally, this strategy should be structured such that it captures dumb order flow and avoids smart order flow, which is not that simple.

One approach is, at any given time, within a short time horizon, to stay on the "right" side of the market, i.e., to have a short-horizon signal indicating the direction of the market and place limit orders accordingly (to buy at the bid if the signal indicates a price increase, and to sell at the ask if the signal indicates a price decrease). If the signal were (magically) 100% correct, this would capture the dumb order flow assuming that the orders get filled. This is a big assumption as for this to be guaranteed, the trader would have to be #1 in the queue among many other market participants placing limit orders at the same price point. This is where high frequency trading comes in - it is essentially all about speed with which orders are placed, canceled, and cancel-replaced. Infrastructure and technology are key in this.

Another possibility is to modulate the short-horizon signal with a longer-horizon signal (which can still be an intraday signal). The longer-horizon signal typically will have a higher cents-per-share 65 than the shorter-horizon signal. Now certain trades can be profitable even with adverse selection, because they are established based on the longer-horizon signal. I.e., they "lose money" in the short term due to adverse selection (as the market trades through the corresponding limit orders), but they make money in a longer term. The market-making aspect of this is valuable as placing a passive limit order as opposed to an aggressive market or limit order saves money. On the other hand, in some cases, if the longer-horizon signal is strong enough and the shorter-horizon signal is in the same direction, a passive limit order would likely not get filled and it may make more sense to place an aggressive order. Such aggressive order flow is not dumb but smart, as it is based on nontrivial shortand long-horizon signals with a positive expected return. 66 And speed still matters.

65 "Cents-per-share" is defined as the realized P&L in cents (as opposed to dollars) divided by the total shares traded (which includes both establishing and liquidating trades). Note that the longer-horizon signal generally has a lower Sharpe ratio than the shorter-horizon signal.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.19. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

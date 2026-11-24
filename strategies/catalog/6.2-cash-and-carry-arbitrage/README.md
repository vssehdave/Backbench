# 6.2 Cash-and-carry arbitrage

- Section: 6.2
- Asset class: Indexes
- Harness status: **not testable: futures** - cash-and-carry needs index futures and a short leg.

## Description (paper)

This strategy (a.k.a. "index arbitrage") aims to exploit price inefficiencies between the index spot 107 price and index futures price. 108 Theoretically, the price of the index futures must equal the spot price accounting for the cost of carry during the life of the futures contract:

$$ F ∗(t, T) = [S(t) −D(t, T)] exp (r (T −t)) $$ (421)

Here: F ∗ ( *t, T) is the theoretical ("fair") price, at time t, of the futures contract with the delivery time T; S ( *t) is the spot value at time t; D ( *t, T) is the sum of (discounted values of) the dividends paid by the underlying stocks between the time *t and delivery; and r is the risk-free rate, which for the sake of simplicity is assumed to be constant from t to delivery. 109 The basis is defined as B(t, T) = F(t, T) −F ∗(t, T) *S ( *t) (422)

where F ( *t, T) is the current price of the futures contract with the delivery time T. If B ( *t, T) *̸ = 0, more precisely, if \| B ( *t, T) *\| exceeds the pertinent transaction costs of executing the arbitrage trade, then there is an arbitrage opportunity. If the basis is positive (negative), the futures price is rich (cheap) compared with the spot price, so the arbitrage trade amounts to selling (buying) the futures and buying (selling) the cash (i.e., the index basket). 110 The position is closed when the basis goes to zero, i.e., the futures price converges to its fair value. Such arbitrage opportunities are short-lived and with the advent of high frequency trading require extremely fast execution. In many cases, the slippage can be prohibitive to execute the trade. 111

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 6.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

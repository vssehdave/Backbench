# 13.2.1 Cross-border tax arbitrage with options

- Section: 13.2.1
- Asset class: Tax arbitrage
- Harness status: **not testable: not a market trading rule** - tax-arbitrage structure needing bond, tax or option data, not a price rule.

## Description (paper)

Absent a tax credit, there is a theoretical upper bound on the value of an American put option (see, e.g., \[Hull, 2012\]):

*V put ( *K, T) ≤ V call ( *K, T) − S 0 + K + D (497)

Here: V put ( *V call) is the price of the put (call) option at time t = 0; K is the strike price; S 0 is the stock price at t = 0; T is the time to maturity; and D is the present value of the dividends during the life of the option. Put options are optimally exercised ex-dividend. Therefore, in the presence of a tax credit, it is expected that put prices should reflect the tax credit, i.e., they should be higher than in the absence of the tax credit (see, e.g., \[McDonald, 2001\]). So the foreign investor can sell the stock cum-dividend (at price S 0 ) and write a deep ITM put option, whose value close to expiration approximately is (here κ is the tax credit rate defined above)

The P&L, once the put is exercised ex-dividend at the strike price K, is the same as with the stock loan/swap strategy discussed above:

$$ P&L = S0 + Vput(K, T) −K = D (1 + \kappa) $$ (499)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 13.2.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

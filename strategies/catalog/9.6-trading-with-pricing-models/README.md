# 9.6 Trading with pricing models

- Section: 9.6
- Asset class: Commodities
- Harness status: **not testable: futures** - needs commodity futures or term-structure data.

## Description (paper)

Commodity futures term structure is nontrivial. One way to model it is via stochastic processes. Let S ( *t) be the spot price, and let X ( *t) = ln( *S ( *t)). Then X ( *t) can be modeled using, e.g., a mean-reverting Brownian motion (i.e., the OrnsteinUhlenbeck process \[Uhlenbeck and Ornstein, 1930\]): 157

$$ dX(t) = \kappa [a −X(t)] dt + \sigma dW(t) $$ (459)

Here the parameters κ (mean-reversion parameter), a (the long-run mean) and σ (log-volatility) are assumed to be constant; and W ( *t) is a Q -Brownian motion, where Q is a risk-free probability measure. 158 The standard claim pricing argument (see, e.g., \[Baxter and Rennie, 1996\], \[Hull, 2012\], \[Kakushadze, 2015a\]) gives for the futures price F ( *t, T) (which is the price at time t of the futures contract with the delivery date T)

F(t, T) = Et(S(T)) (460) $$ ln(F(t, T)) = Et(X(T)) + 1 $$

2 V t ( X ( T )) (461)

Here E t ( *·) and V t ( *·) are the conditional expectation and variance, respectively, at time t. This gives:

ln( *F ( *t, T)) $$ = $$ exp (−\kappa(T −t)) X(t) + a [1 −exp (−\kappa(T −t))] + + 4κ [1 −exp (−2\kappa(T −t))] (462)

The parameters κ, a, σ can be fitted using historical data (e.g., using nonlinear least squares). Then the current market price can be compared to the model price to identify the futures that are rich (sell signal) and cheap (buy signal) compared with the model prediction. Here two cautionary remarks are in order. First, the model fit could work in-sample but have no predictive power out-of-sample, so the forecasting power needs to be ascertained (see, e.g., \[Paschke and Prokopczuk, 2012\]). Second, a priori we could write down any reasonable term structure model with desirable qualitative properties (e.g., mean-reversion) and fit the parameters using historical data without any reference to an underlying stochastic dynamics whatsoever, including using, e.g., "black-box" machine learning techniques. So long as the model works out-of-sample, there is no magic bullet here and "fancy" does not equal "better".

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 9.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

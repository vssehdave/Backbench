# 6.3 Dispersion trading in equity indexes

- Section: 6.3
- Asset class: Indexes
- Harness status: **not testable: options chains** - dispersion trading uses index and single-stock options.

## Description (paper)

This strategy takes long positions on volatilities of the index constituents and a short position on index volatility. It is rooted in an empirical observation that, for

Wang, 2002\], \[Edwards, 1988\], \[Frino et al, 2004\], \[Graham and Pirie, 1994\], \[Hautcoeur, 2006\], \[Illueca and Lafuente, 2003\], \[Kenett et al, 2013\], \[Lamoureux and Wansley, 1987\], \[Larsen and Resnick, 1998\], \[Lo, 2016\], \[Schwartz and Laatsch, 1991\], \[Spyrou, 2005\], \[Yo, 2001\].

107 "Spot" refers to the current value of the index based on the current prices of its constituents. "Cash" refers to the underlying index portfolio. This is common trader lingo.

110 Selling the futures poses no issues. However, selling the cash can be problematic with shortselling issues such as hard-to-borrow securities, etc. Continuously maintaining a sizable dollarneutral book which is long cash and short futures can help circumvent such issues.

111 In some cases incomplete baskets approximating the index can be executed to reduce the transaction costs, e.g., in market cap weighted indexes, by omitting lower cap (and thus less liquid) stocks. However, such mishedges also increase the risk of losing money on the trade.

the most part, 112 the implied volatility e σ I from index options is sizably higher than

the theoretical index volatility σ I given by

I =

N X $$ i,j=1 $$ iwj\sigmai\sigmaj\rhoij (423)

where w i are the weights of the stocks in the index, σ i are their implied volatilities

from single-stock options, and ρ ij is the sample correlation matrix ( *ρ ii = 1) 113

computed based on a time series of historical returns. 114 Put differently, the index

options are priced higher than the price corresponding to the aforesaid theoretical volatility. So, a basic strategy can be structured as follows. For each stock in the index we have a long position in n i (near-ATM) single-stock option straddles (whose payoffs are based on the stock prices P i), and we have a short position in a (nearATM) option straddle for the index (whose payoffis based on the index level P I - see below), where ni = *i P I N i=1 SiPi

(424)

Here: S i is shares outstanding for stock i (we are assuming the index is market

cap weighted); and P I is the index level. With this definition of n i, we have P I = *N*

i =1 n i P i, so the index option straddle payoffmatches the individual single-stock

option straddle payoffs as closely as possible. 115 All options have approximately 1 month until the expiration, and all positions remain open until the expiration. 116

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 6.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

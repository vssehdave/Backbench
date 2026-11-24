# 3.6 Multifactor portfolio

- Section: 3.6
- Asset class: Stocks
- Harness status: **not testable: cross-sectional universe** - combines several cross-sectional factors over a stock universe.

## Description (paper)

This strategy amounts to buying and shorting stocks based on multiple factors such as value, momentum, etc. For instance, usually value and momentum are negatively correlated and combining them can add value (see, e.g., \[Asness, Moskowitz and Pedersen, 2013\]). There is a variety of ways in which F \> 1 factors can be combined. 46 The simplest way is to diversify the exposure to the F factors with some weights w A, where A = 1 ,..., F labels the factors. That is, if I is the total investment level, then the F portfolios (each built as above based on the corresponding factor) are allocated the investment levels I A = w A × I, where (assuming all w A \> 0)

F X

A=1

Thus, one can simply take uniform weights w A = 1 */F, albeit this may not be the most optimal weighting scheme. E.g., similarly to Subsection 3.1, there are weighting

Thorley, 2010\], \[Frazzini and Pedersen, 2014\], \[Fu, 2009\], \[Garcia-Feij´oo et al, 2015\], \[Li, Sullivan and Garcia-Feij´oo, 2014\], \[Li, Sullivan and Garcia-Feij´oo, 2016\], \[Merton, 1987\].

schemes with wA \propto1/\sigmaA, wA \propto1/\sigma2

*A, etc., where σ A is the historical volatility for the corresponding factor portfolio (uniformly normalized, e.g., per dollar invested). 47

Alternatively, consider F rankings of stocks based on the F factors. One can now combine these rankings in various ways to blend the factors. E.g., in the case of two factors, momentum and value, one can take the top (winners) and bottom (losers) quintiles by momentum and further split them into top half and bottom half, respectively, by value. Or one can take the top and bottom quintiles by value and split them by momentum. 48 Yet another way is to define demeaned ranks sAi = rank(fAi) −1

N

N X $$ j=1 $$ rank( *f Aj) (276)

where f Ai is the numeric value of the factor labeled by A (e.g., momentum) for the stock labeled by i ( *i = 1 ,..., N). One can then simply average the ranks: $$ si = 1 $$

F

F X

A=1 *Ai (277)

The combined "score" s i can have ties, which, if need be (e.g., if there is an ambiguity at the border of the top decile) can be resolved, e.g., simply by giving preference to one of the factor rankings. Averaging over s Ai simply minimizes the sum of squares of the Euclidean distances between the N -vector s i and the K N -vectors s Ai. One can introduce nonuniform weights into this sum (which would amount to a weighted average in Eq. (277)), or even use a different definition of the distance (e.g., the Manhattan distance), which would complicate the problem computationally. Etc. 49

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

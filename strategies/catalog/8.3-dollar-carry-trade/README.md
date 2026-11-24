# 8.3 Dollar carry trade

- Section: 8.3
- Asset class: Foreign exchange
- Harness status: **not testable: FX** - needs FX spot or forward data; the alpaca and kraken data kinds do not provide it.

## Description (paper)

This strategy is based on the average cross-sectional forward discount D ( *t, T) (see, e.g., \[Lustig, Roussanov and Verdelhan, 2014\]) for a basket of N foreign currencies: $$ D(t, T) = 1 $$

N

N X $$ i=1 $$ *D i ( *t, T) (444)

where D i ( *t, T) is the forward discount for the currency labeled by i = 1 ,..., N. This strategy then goes long (short), with equal weights, all N foreign currency forwards when D ( *t, T) is positive (negative), where T can be 1 , 2 , 3 , 6 , 12 months. Empirical evidence suggests that this strategy relates to the state of the U.S. economy, to wit, when the U.S. economy is weak, the average forward discount tends to be positive. 148

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

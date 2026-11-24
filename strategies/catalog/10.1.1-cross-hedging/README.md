# 10.1.1 Cross-hedging

- Section: 10.1.1
- Asset class: Futures
- Harness status: **not testable: futures** - needs futures data and positions.

## Description (paper)

Sometimes a futures contract for the asset to be hedged may not be available. In such cases, the trader may be able to hedge using a futures contract for another asset with similar characteristics. 160 At maturity T, the payoffof the cross-hedged position established at time t (assuming the short futures position with the unit hedge ratio) is given by:

S(T) −F(T, T) + F(t, T) =

\[ *S ∗ ( *T) − F ( *T, T)\] + \[ *S ( *T) − S ∗ ( *T)\] + F ( *t, T) (463)

Here: the subscript ∗ indicates that the underlying asset of the futures contract is different from the hedged asset; S ( *t) is the spot price; F ( *t, T) is the futures price; the first term on the r.h.s. represents the basis risk stemming from the difference at delivery between the futures and the spot prices; and the second term represents the difference twixt the two underlying prices. In practice, the optimal hedge ratio may not be 1 and can be estimated via, e.g., a serial regression or some other method. 161

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 10.1.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

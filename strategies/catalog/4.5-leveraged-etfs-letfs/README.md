# 4.5 Leveraged ETFs (LETFs)

- Section: 4.5
- Asset class: Exchange-traded funds
- Harness status: **not testable: multiple instruments** - shorts a leveraged ETF and a leveraged inverse ETF and holds a Treasury ETF; needs short selling.

## Description (paper)

A leveraged (inverse) ETF seeks to double or triple (the inverse of) the daily return of

its underlying index. 82 To maintain a daily leverage of 2 *× or 3 *×, LETFs rebalance

81 An equivalent but more symmetrical measure is Y = IBS − 1 */ 2 = ( *P C − P ∗) */ ( *P H − P L), where P ∗ = ( *P H + P L) */ 2. Note that Y ranges from 1 */ 2 for P C = P H to − 1 */ 2 for P C = P L.

every day, which requires buying on the days when the market is up and selling when the market is down. This can result in a negative drift in the long term, which can be exploited by shorting both a leveraged ETF and a leveraged inverse ETF (both with the same leverage and for the same underlying index) and investing the proceeds into, e.g., a Treasury ETF. This strategy can have a significant downside risk in the short term if one of the short ETF legs has a sizable positive return.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

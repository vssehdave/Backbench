# 8.2.1 High-minus-low carry

- Section: 8.2.1
- Asset class: Foreign exchange
- Harness status: **not testable: FX** - needs FX spot or forward data; the alpaca and kraken data kinds do not provide it.

## Description (paper)

The carry strategy discussed above can be applied to individual foreign currencies. It can also be applied cross-sectionally, to multiple foreign currencies. Let s ( *t) = ln( *S ( *t)) (log spot FX rate) and f ( *t, T) = ln( *F ( *t, T)) (log forward FX rate). The forward discount D ( *t, T) is defined as D(t, T) = s(t) −f(t, T) (442) Pursuant to CIRP, Eq. (441), we have D(t, T) = ln  1 + r f 1 + r d  *≈ r f − r d (443)

For a positive forward discount, we buy a forward (i.e., borrow the domestic currency and invest in the foreign currency), and the higher the forward discount, the more profitable the strategy. For a negative forward discount, we sell a forward (i.e., borrow the foreign currency and invest in the domestic currency), and the lower the forward discount, the more profitable the strategy. So, we can construct a cross-sectional trade (including a zero-cost, i.e., dollar-neutral trade - see, e.g., \[Lustig, Roussanov and Verdelhan, 2011\]) by buying forwards on currencies in some top quantile 147 by forward discount and selling forwards on currencies in the corresponding bottom quantile. The forwards can, e.g., be one-month forwards.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.2.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

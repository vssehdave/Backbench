# 5.3 Barbells

- Section: 5.3
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

In this strategy all purchased bonds are concentrated in two maturities T 1 (short maturity) and T 2 (long maturity), so this portfolio is a combination of two bullet strategies. This strategy takes advantage of the higher yields from the long-maturity bonds while hedging the interest rate risk with the short-maturity bonds: if the interest rates rise, the long-maturity bonds will lose value, but the proceeds from the short-maturity bonds can be reinvested at higher rates. 88 The modified duration (call it D) of the barbell strategy is the same as the modified duration (call it *D ∗) of a bullet strategy with a mid-range maturity (call it T ∗, T 1 \< T ∗ \< T 2 ). However, the convexity (call it C) of the barbell strategy is higher than the convexity (call it C ∗) of this bullet strategy. Intuitively this can be understood by noting that modified duration scales approximately linearly with maturity, while convexity scales approximately quadratically with maturity. For illustrative purposes and simplicity, let us consider a barbell strategy consisting of w 1 dollars' worth of zerocoupon bonds with short maturity T 1 and w 2 dollars' worth of zero-coupon bonds with long maturity T2 (each bond has $1 face value). Furthermore, let us assume continuous compounding and a constant yield Y. We then have $$ D = ew1 T1 + ew2 T2 $$ e *w 1 + e *w 2 (390)

T∗= D∗= D (391) $$ C = ew1 T 2 $$ 1 + e *w 2 T 2 e *w 1 + e *w 2 (392)

∗= T 2 *∗ (393)

where e *w 1 = w 1 exp( *− T 1 Y) and e *w 2 = w 2 exp( *− T 2 Y). Straightforward algebra gives

*C − C ∗ = e *w 1 e *w 2 ( ew1 + ew2)2 (T2 −T1)2 > 0 (394)

Higher convexity of the barbell portfolio provides a better protection against parallel shifts in the yield curve. However, this comes at the expense of a lower overall yield.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

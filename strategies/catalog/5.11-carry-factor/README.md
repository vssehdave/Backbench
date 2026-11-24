# 5.11 Carry factor

- Section: 5.11
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

Carry is defined as the return from the appreciation of the bond value as the bond rolls down the yield curve (see, e.g., \[Beekhuizen et al, 2016\], \[Koijen, Moskowitz, Pedersen and Vrugt, 2018\]): 98 C(t, t + ∆t, T) = P(t + ∆t, T) −P(t, T) *P ( *t, T) (413)

Here ∆ *t is the period over which carry is computed. A simplification arises if we assume that the entire term structure of the interest rates stays constant, i.e., the yield R ( *t, T) = f ( *T − t) is a function of only T − t (i.e., time to maturity). Then, at time t + ∆ *t the yield is R ( *t + ∆ *t, T) = R ( *t, T − ∆ *t). So, we have 99 *C ( *t, t + ∆ *t, T) $$ = $$

*P ( *t + ∆ *t, T) *\| R ( *t +∆ *t,T) − P ( *t, T) *\| R ( *t,T) *P ( *t, T) *\| R ( *t,T) $$ = $$

$$ = $$ *R ( *t, T) ∆ *t + C roll ( *t, t + ∆ *t, T) (414)

where (taking into account the definition of the modified duration, Eq. (385)) *C roll ( *t, t + ∆ *t, T) $$ = $$

*P ( *t + ∆ *t, T) *\| R ( *t,T − ∆ *t) − P ( *t + ∆ *t, T) *\| R ( *t,T) *P ( *t, T) *\| R ( *t,T) $$ \approx $$

$$ \approx $$ *− ModD( *t, T) \[ *R ( *t, T − ∆ *t) − R ( *t, T)\] (415)

So, if the term structure of the interest rates is constant, then carry C ( *t, t + ∆ *t, T) receives two contributions: i) R ( *t, T) ∆ *t from the bond yield; and ii) C roll ( *t, t +∆ *t, T) from the bond rolling down the yield curve. A zero-cost strategy can be built, e.g., by buying bonds in the top decile by carry and selling bonds in the bottom decile.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.11. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

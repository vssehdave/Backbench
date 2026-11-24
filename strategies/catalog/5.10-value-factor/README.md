# 5.10 Value factor

- Section: 5.10
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

"Value" for bonds (see, e.g., \[Correia, Richardson and Tuna, 2012\], \[Houweling and van Vundert, 2017\], \[L'Hoir and Boulhabel, 2010\]) is trickier to define than for stocks. One way is to compare the observed credit spread 96 to a theoretical prediction therefor. One way to estimate the latter is, e.g., via a linear cross-sectional (across *N bonds labeled by i = 1 ,..., N) regression \[Houweling and van Vundert, 2017\]: Si =

K X $$ r=1 $$ \betar Iir + \gamma Ti + ϵi (410) *∗ i = S i − ϵ i (411)

Here: S i is the credit spread; I ir is a dummy variable ( *I ir = 1 if the bond labeled by i has credit rating r; otherwise, I ir = 0) for bond credit rating r (which labels *K credit ratings present among the N bonds, which can be one of the 21 credit ratings); 97 T i are bond maturities; β r , γ are the regression coefficients; ϵ i are the regression residuals; and S ∗*

*i is the fitted (theoretical) value of the credit spread. The N × K matrix I ir has no columns with all zeros (so K can be less than 21). Note that by definition, since each bond has one and only one credit rating, we have

K X $$ r=1 $$ $$ Iir = 1 $$ (412)

so the intercept is subsumed in I ir (which is why there is no separate regression coefficient for the intercept). Next, value is defined as V i = ln( *S i /S ∗ i ) or Vi = ϵi/S∗ $$ i = $$ *i /S ∗*

*i − 1, and the bonds in the top decile by V i are selected for the portfolio.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.10. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

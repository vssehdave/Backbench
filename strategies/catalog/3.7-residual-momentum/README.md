# 3.7 Residual momentum

- Section: 3.7
- Asset class: Stocks
- Harness status: **not testable: cross-sectional universe** - regresses a stock universe on factors; needs cross-sectional data.

## Description (paper)

This is the same as the price-momentum strategy with the stock returns R i ( *t) replaced by the residuals ϵ i ( *t) of a serial regression of the stock returns R i ( *t) over, e.g., the 3 Fama-French factors MKT( *t), SMB( *t), HML( *t), 50 with the intercept (see,

47 Another approach is to fix the weights w A by optimizing a portfolio of the F expected returns corresponding to the F factors (using an invertible F × F covariance matrix for these returns).

$$ Ri(t) = \alphai + \beta1,i MKT(t) + \beta2,i SMB(t) + \beta3,i HML(t) + ϵi(t) $$ (278)

The regression is run over a 36-month period \[Blitz, Huij and Martens, 2011\] (with the 1-month skip period) to estimate the regression coefficients α i, β 1 ,i, β 2 ,i, β 3 ,i. Once the coefficients are estimated, the residuals can be computed for the 12-month formation period (again, with the 1-month skip period):

ϵi(t) = Ri(t) −\beta1,i MKT(t) −\beta2,i SMB(t) −\beta3,i HML(t) (279)

Note that α i is not included in this computation of the residuals for the 12-month formation period as α i was computed for the 36-month period. These residuals *ϵ i ( *t) are then used to compute, e.g., the risk-adjusted residual returns e *R risk.adj*

*i (here *S = 1 and T = 12; the holding period typically is 1 month, but can be longer): *mean i $$ = 1 $$

T

S + T − 1 X t=S *ϵ i ( *t) (280) e *R risk.adj i = ϵ mean i e\sigmai (281) e\sigma2 $$ i = $$ *T − 1

S + T − 1 X t=S ( *ϵ i ( *t) − ϵ mean i) 2 (282)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

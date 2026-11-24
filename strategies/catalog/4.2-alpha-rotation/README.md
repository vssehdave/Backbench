# 4.2 Alpha rotation

- Section: 4.2
- Asset class: Exchange-traded funds
- Harness status: **not testable: cross-sectional universe** - rotates among ETFs by alpha from a factor regression; needs several series and factor data.

## Description (paper)

This is the same as the sector momentum rotation strategy with the cumulative ETF returns R cum*

*i replaced by ETF alphas α i, which are the regression coefficients corresponding to the intercept in a serial regression of the ETF returns 77 R i ( *t) over, e.g., the 3 Fama-French factors MKT( *t), SMB( *t), HML( *t) (see fn. 50): 78

$$ Ri(t) = \alphai + \beta1,i MKT(t) + \beta2,i SMB(t) + \beta3,i HML(t) + ϵi(t) $$ (364)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

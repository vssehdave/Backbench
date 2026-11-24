# 3.10 Mean-reversion - weighted regression

- Section: 3.10
- Asset class: Stocks
- Harness status: **not testable: cross-sectional universe** - cross-sectional weighted regression over a stock universe; needs short selling.

## Description (paper)

Mean-reversion - weighted regression

The conditions (310) satisfied by the demeaned returns when the loadings matrix is binary simply mean that these returns are cluster-neutral, i.e., orthogonal to the K N -vectors v ( *A) comprising the columns of Λ *iA. Such orthogonality can be defined for any loadings matrix, not just a binary one. So, we can consider a generalization where the loadings matrix, call it Ω *iA, may have some binary columns, but generally it need not. The binary columns, if any, can, e.g., be industry (or sector) based risk factors; the non-binary columns are interpreted as some non-industry based risk factors; and the orthogonality condition

N X $$ i=1 $$

e *R i Ω *iA , A = 1 ,..., K (313)

can be satisfied if the twiddled returns e *R i are related to the residuals ε i of the regression of R i over Ω *iA with some (generally nonuniform) regression weights z i via

$$ eR = Z \epsilon $$ (314) \epsilon = R −ΩQ−1 ΩT Z R (315) Z = diag(zi) (316) *Q = Ω *T Z Ω (317)

If the intercept is included in Ω *iA (i.e., a linear combination of the columns of Ω *iA equals the unit N -vector ν), then we automatically have

N X $$ i=1 $$ $$ eRi = 0 $$ (318)

The weights z i can, e.g., be taken as z i = 1 */σ 2

*i, where σ i are historical volatilities. 54

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.10. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

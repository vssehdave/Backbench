# 3.9.1 Mean-reversion - multiple clusters

- Section: 3.9.1
- Asset class: Stocks
- Harness status: **not testable: cross-sectional universe** - cross-sectional mean reversion across multiple clusters; needs a stock universe and short selling.

## Description (paper)

The mean-reversion strategy of Subsection 3.9 can be readily generalized to the case where we have K \> 1 clusters such that stocks within each cluster are historically highly correlated. 53 We can simply treat clusters independently from each other and construct a mean-reversion strategy following the above procedure in each cluster. Then, e.g., we can allocate investments to these K independent strategies uniformly.

There is a neat way of treating all clusters in a "unified" fashion using a linear regression. Let the K clusters be labeled by A = 1 ,..., K. Let Λ *iA be an N × K matrix such that if the stock labeled by i ( *i = 1 ,..., N) belongs to the cluster labeled by A, then Λ *iA = 1; otherwise, Λ *iA = 0. We will assume that each and every stock belongs to one and only one cluster (so there are no empty clusters):

NA =

N X $$ i=1 $$ \LambdaiA > 0 (299)

N =

K X

A=1

A (300)

$$ iA = \deltaG(i),A $$ (301) *G: \{ 1 ,..., N \} 7→\{ 1 ,..., K \} (302)

Here: G is the map between stocks and clusters; and Λ *iA is the loadings matrix.

Now consider a linear regression of the stock returns R i over Λ *iA (without the intercept and with unit weights): Ri =

K X

A=1 \LambdaiA fA + \epsiloni (303)

where f A are the regression coefficients given by (in matrix notation, where R is the *N -vector R i, f is the K -vector f A, and Λ is the N × K matrix Λ *iA)

f = Q−1 \LambdaT R (304) $$ Q = \LambdaT \Lambda $$ (305)

and ε i are the regression residuals. For binary Λ *iA given by Eq. (301), these residuals are nothing but the returns R i demeaned w.r.t. to the corresponding cluster:

$$ \epsilon = R −\Lambda Q−1 \LambdaT R $$ (306) *Q AB = N A δ AB (307)

RA = *A*

X *j ∈ J A j (308) \epsiloni = Ri −RG(i) = eRi (309)

where R A is the mean return for the cluster labeled by A, and e *R i is the demeaned return obtained by subtracting from R i the mean return for the cluster labeled by *A = G ( *i) to which the stock labeled by i belongs: J A = \{ i \| G ( *i) = A \} ⊂\{ 1 ,..., N \}.

The demeaned returns are cluster-neutral, i.e.,

N X $$ i=1 $$

eRi \LambdaiA = 0, *A = 1 ,..., K (310)

Also, note that we automatically have (so D i given by Eq. (297) satisfy Eq. (296))

N X $$ i=1 $$ $$ eRi \nui = 0 $$ (311)

where ν i ≡ 1, i = 1 ,..., N, i.e., the N -vector ν is the unit vector. In the regression language, ν is the intercept. We did not have to add the intercept to the loadings matrix Λ as it is already subsumed in it:

K X

A=1 $$ \LambdaiA = \nui $$ (312)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.9.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

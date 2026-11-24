# 4.3 R-squared

- Section: 4.3
- Asset class: Exchange-traded funds
- Harness status: **not testable: cross-sectional universe** - uses regression R-squared across ETFs; needs factor returns and several series.

## Description (paper)

Empirical studies for mutual funds (see, e.g., \[Amihud and Goyenko, 2013\], \[Ferson and Mo, 2016\]) and ETFs (see, e.g., \[Garyn-Tal, 2014a\], \[Garyn-Tal, 2014b\]) suggest that augmenting alpha by an indicator based on R 2 of a serial regression of the returns R i ( *t) over multiple factors, e.g., the 3 Fama-French factors MKT( *t), SMB( *t), HML( *t) plus Carhart's momentum factor MOM( *t) (see fn. 50), adds value in forecasting future returns. Thus, from the serial regression

$$ Ri(t) = \alphai + \beta1,i MKT(t) + \beta2,i SMB(t) + \beta3,i HML(t) + \beta4,i MOM(t) + ϵi(t) (365) $$

we can estimate α i (the regression coefficients corresponding to the intercept) and the regression R 2, which is defined as ("SS" stands for "sum of squares"): R2 = 1 −SSres SS *tot (366) SS *res =

N X $$ i=1 $$ *i ( *t) (367) SS *tot =

N X $$ i=1 $$ ( *R i ( *t) − R ( *t)) 2 (368) $$ R(t) = 1 $$

N

N X $$ i=1 $$ *R i ( *t) (369)

An R-squared strategy then amounts to overweighing ETFs with higher "selectivity"

(defined as 1 *− R 2 \[Amihud and Goyenko, 2013\]) and underweighing ETFs with lower "selectivity". E.g., one can first sort ETFs into quintiles by R 2, and then sort ETFs in each such quintile into further sub-quintiles by alpha (resulting in 25 groups of ETFs). One can then, e.g., buy ETFs in the group corresponding to the lowest R 2

quintile and its highest alpha sub-quintile and sell ETFs in the group corresponding

to the highest R 2 quintile and its lowest alpha sub-quintile. Other variations are possible. Finally, the estimation period and the returns for R 2 can be the same as in the alpha rotation strategy (see Subsection 4.2 and fn. 77). However, longer estimation periods can be considered, especially if R i ( *t) are monthly returns. 79

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

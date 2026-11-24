# 4.3 R-squared

- Section: 4.3
- Asset class: Exchange-traded funds
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/4.3-r-squared/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

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

## xs harness result

Construction: Long low R-squared with high alpha, short high R-squared with low alpha, among sector ETFs (4-factor regression).
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: proxy: ETF-mimicking factors (SPY, IWM-SPY, IVE-IVW, MTUM-SPY) instead of Fama-French and Carhart; survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (about one ETF per leg).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -1.7% | -2.3% | -0.38 |
| equal-weight | +7.3% | +7.2% | 1.38 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.27%, turnover 5.1x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +3.4% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | -5.7% | +9.9% | +11.5% | +0.0% | -1.88 | 0.36% |
| 2018-07-02..2018-12-31 | +2.2% | -7.6% | -6.9% | +0.0% | 0.43 | 0.42% |
| 2019-07-01..2019-12-31 | +0.3% | +8.8% | +10.9% | +0.0% | 0.11 | 0.25% |
| 2020-07-01..2020-12-31 | -7.0% | +20.0% | +22.1% | +0.0% | -1.24 | 0.27% |
| 2021-07-01..2021-12-31 | +0.1% | +10.5% | +11.7% | +0.0% | 0.06 | 0.20% |
| 2022-07-01..2022-12-30 | +4.3% | +3.9% | +2.3% | +0.0% | 0.67 | 0.21% |
| 2023-07-03..2023-12-29 | -2.4% | +6.1% | +8.0% | +0.0% | -0.45 | 0.31% |
| 2024-07-01..2024-12-31 | -2.3% | +7.2% | +8.4% | +0.0% | -0.25 | 0.25% |
| 2025-07-01..2025-12-31 | -4.7% | +6.8% | +11.0% | +0.0% | -0.88 | 0.19% |

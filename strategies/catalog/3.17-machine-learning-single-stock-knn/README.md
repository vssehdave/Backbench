# 3.17 Machine learning - single-stock KNN

- Section: 3.17
- Asset class: Stocks
- Harness status: **not testable: needs high/low/volume** - features use volume and a KNN model; decide() receives closes only.

## Description (paper)

Some strategies rely on machine learning techniques, such as the k-nearest neighbor (KNN) algorithm (see, e.g., \[Altman, 1992\], \[Samworth, 2012\]), to predict future stock returns (the target variable) based on a set of predictor (feature) variables, which can be based on technical, fundamental and/or some other data. The strategy we describe here is a single-stock strategy, i.e., for each stock the target variable is predicted using the price and volume data only for this stock (but no cross-sectional data, i.e., no data for other stocks). The target variable Y ( *t) is defined as the cumulative return over the next T trading days (as above, the ascending integer values of t, which is measured in trading days, correspond to going back in time): $$ Y (t) = P(t −T) $$ *P ( *t) *− 1 (332)

The predictor variables X a ( *t), a = 1 ,..., m, are defined using prices P ( *t ′) and volumes V ( *t ′) at times t ′ before t (i.e., t ′ \> t), so they are out-of-sample. Examples of such variables are moving averages of the price and volume of varying lengths: $$ X1(t) = 1 $$

T 1 X $$ s=1 $$ *V ( *t + s) (333) $$ X2(t) = 1 $$

T 2 X $$ s=1 $$ *P ( *t + s) (334) $$ X3(t) = 1 $$

T 3 X $$ s=1 $$ *P ( *t + s) (335) ... (336)

The predictor variables are further normalized to lie between 0 and 1: e Xa(t) = Xa(t) −X− *a + *a − X − a (337) where X + *a and X −*

*a are the maximum and minimum values of X a ( *t) over the training period. The final ingredient is the number k of the nearest neighbors (see below). For a given value of t we can take k nearest neighbors of the m -vector e *X a ( *t) among the m -vectors e *X a ( *t ′), t ′ = t + 1 , t + 2 ,..., t + T ∗, using the KNN algorithm (here

*T ∗ is the sample size). For KNN we can use the Euclidean distance D ( *t, t ′) between

e *X a ( *t) and e *X a ( *t ′) defined as $$ [D(t, t′)]2 = $$ *m X $$ a=1 $$

( e *X a ( *t) − e *X a ( *t ′)) 2 (338)

However, we can use some other distance (e.g., the Manhattan distance). Let the k nearest neighbors of e *X a ( *t) be e *X a ( *t ′*

*α ( *t)), α = 1 ,..., k. (Note that the k values t ′*

\alpha(t) depend on t.) Then we can define the predicted value Y ( *t) simply as an average of the corresponding realized values Y ( *t ′ \alpha(t)): $$ Y(t) = 1 $$ *k k X $$ \alpha=1 $$ *Y ( *t ′ \alpha(t)) (339)

Alternatively, we can, e.g., consider a linear model $$ Y(t) = $$ *k X $$ \alpha=1 $$ *Y ( *t ′ \alpha(t)) wα + v (340)

and fix the coefficients w α and v by running a regression 59 of the realized values *Y ( *t) over Y ( *t ′*

*α ( *t)) for some number - call it M - of values of t. I.e., we pull Y ( *t) for these values of t into an M -vector and regress it over the M × k matrix of the corresponding values Y ( *t ′*

*α ( *t)). The coefficients of this regression are w α and v. The advantage of using Eq. (339) is simplicity - there are no parameters to train in this case. We still have to backtest the strategy (see below) out-of-sample. The disadvantage is that equally weighting contributions of all k nearest neighbors could be suboptimal. In this regard, there are various (e.g., distance-based) weighting schemes one may consider. Nontrivial weighting is precisely what Eq. (340) intends to capture. However, this requires training and cross-validation (using metrics such as root mean square error), and the fitted parameters w α and v can be (and often are) out-of-sample unstable. The data can be split, e.g., 60% for training and 40% for cross-validation. Ultimately, the strategy must backtest well out-of-sample.

The signal at t = 0 can be defined using the predicted value Y = Y (0), which is the expected return for the next T days. For single-stock trading 60 one can simply define thresholds for establishing long and short trades, and liquidating existing

59 We can run this regression without the intercept, in which case we only have the coefficients *w α, or with the intercept, in which case we also have the coefficient v.

60 Alternatively, one can use expected returns Y i computed for N stocks (where N ≫ 1) using a machine learning algorithm as above and then use these expected returns in multi-stock crosssectional strategies such as mean-reversion/statistical arbitrage.

positions, e.g., as follows: 61

Signal =

    

   

Establish long position if Y \> z 1

Liquidate long position if Y ≤ z 2 Establish short position if Y \< − z 1 Liquidate short position if Y ≥− z 2

(341)

Here, z 1 and z 2 are trader-defined thresholds. This signal must be backtested out

of-sample. The number k of nearest neighbors can be optimized using a backtest (by trying a set of values of k). Alternatively, one can use a common heuristic, e.g., *k = floor( *√ T ∗) or k = ceiling( *√ T ∗). Also see, e.g., \[Hall, Park and Samworth, 2008\].

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.17. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

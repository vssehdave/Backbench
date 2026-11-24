# 3.20 Alpha combos

- Section: 3.20
- Asset class: Stocks
- Harness status: **not testable: not specified by the paper** - The paper's alpha combos need a library of many alphas, which it does not specify; there is nothing to combine without inventing it.

## Description (paper)

With technological advances - hardware becoming cheaper and more powerful - it is now possible to data mine hundreds of thousands and even millions of alphas using machine learning methods. Here the term "alpha" - following common trader lingo - generally means any reasonable "expected return" that one may wish to trade on and is not necessarily the same as the "academic" alpha. 67 In practice, often the detailed information about how alphas are constructed may not even be available, e.g., the only data available could be the position data, so "alpha" then is a set of instructions to achieve certain stock (or some other instrument) holdings by some times t 1 , t 2 ,... Also, "machine learning" here refers to sophisticated methods that go beyond single-stock methods such as those discussed in Subsection 3.17 and involve cross-sectional analyses based on price-volume as well as other types of data (e.g., market cap, some other fundamental data such as earnings, industry classification data, sentiment data, etc.) for a large number of stocks (typically, a few thousand and up). 101 explicit examples of such quantitative trading alphas are given in \[Kakushadze, 2016\]. 68 The flipside is that these ubiquitous alphas are faint, ephemeral and cannot be traded on their own as any profit on paper would be eaten away by trading costs. To mitigate this, one combines a large number of such alphas and trades the so-combined "mega-alpha". Hence "alpha combo" strategies.

This is not critical, but for definiteness let us assume that all alphas trade the same underlying instruments, even more concretely, the same universe of (say, 2,500) most liquid U.S. stocks. Each alpha produces desired holdings for this trading universe. What we need is the weights with which to combine individual alphas, whose number N can be large (in hundreds of thousands or even millions). 69 Here

long-horizon institutional traders (mutual funds, pension funds, etc.), whose outlook can be months or years and who are not concerned about a few pennies' worth of difference in the execution price on short horizons (i.e., this is only "short-term dumb" order flow). For a more detailed discussion, see, e.g., \[Kakushadze, 2015d\], \[Lo, 2008\]. For some literature on high frequency trading and marketmaking, see, e.g., \[Aldridge, 2013\], \[Anand and Venkataraman, 2016\], \[Avellaneda and Stoikov, 2008\], \[Baron et al, 2014\], \[Benos et al, 2017\], \[Benos and Sagade, 2016\], \[Biais and Foucault, 2014\], \[Biais, Foucault and Moinas, 2014\], \[Bowen, Hutchinson and O'Sullivan, 2010\], \[Bozdog et al, 2011\], \[Brogaard and Garriott, 2018\], \[Brogaard et al, 2015\], \[Brogaard, Hendershott and Riordan, 2014\], \[Budish, Cramton and Shim, 2015\], \[Carrion, 2013\], \[Carrion and Kolay, 2017\], \[Easley, L´opez de Prado and O'Hara, 2011\], \[Easley, L´opez de Prado and O'Hara, 2012\], \[Egginton, Van Ness and Van Ness, 2016\], \[Hagstr¨omer and Nord´en, 2013\], \[Hagstr¨omer, Nord´en and Zhang, 2014\], \[Harris and Namvar, 2016\], \[Hasbrouck and Saar, 2013\], \[Hendershott, Jones and Menkveld, 2011\], \[Hendershott, Jones and Menkveld, 2013\], \[Hendershott and Riordan, 2013\], \[Hirschey, 2018\], \[Holden and Jacobsen, 2014\], \[Jarrow and Protter, 2012\], \[Khandani and Lo, 2011\], \[Kirilenko et al, 2017\], \[Korajczyk and Murphy, 2017\], \[Kozhan and Tham, 2012\], \[Li et al, 2014\], \[Madhavan, 2012\], \[Menkveld, 2013\], \[Menkveld, 2016\], \[Muthuswamy et al, 2011\], \[O'Hara, 2015\], \[Pagnotta and Philippon, 2012\], \[Riordan and Storkenmaier, 2012\], \[Van Kervel and Menkveld, 2017\].

is a procedure for fixing the alpha weights w i, i = 1 ,..., N \[Kakushadze and Yu, 2017b\] (also see \[Kakushadze and Yu, 2018a\]): *• 1) Start with a time series of realized alpha returns 70 R is, i = 1 ,..., N, s = 1 ,..., M + 1. *• 2) Calculate the serially demeaned returns X is = R is − M +1

M +1

s=1 Ris. *• 3) Calculate sample variances of alpha returns 71 σ 2 $$ i = $$ *M*

M +1 $$ s=1 X2 $$

*is. *• 4) Calculate the normalized demeaned returns Y is = X is /σ i. *• 5) Keep only the first M columns in Y is: s = 1 ,..., M. *• 6) Cross-sectionally demean Y is: Λ *is = Y is − 1 *N*

N

j=1 Yjs. *• 7) Keep only the first M − 1 columns in Λ *is: s = 1 ,..., M − 1. *• 8) Take the expected alpha returns E i and normalize them: e *E i = E i /σ i. One (but by far not the only) way of computing expected alpha returns is via d -day moving averages (note that d need not be the same as T): $$ Ei = 1 $$ *d d X $$ s=1 $$ *is (360)

*• 9) Calculate the residuals e *ε i of the regression (without the intercept and with unit weights) of e *E i over Λ *is.

*• 10) Set the alpha portfolio weights to w i = η e *ε i /σ i. *• 11) Set the normalization coefficient η such that P *N $$ i=1 |wi| = 1. $$

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.20. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

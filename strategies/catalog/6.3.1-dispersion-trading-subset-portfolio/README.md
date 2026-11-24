# 6.3.1 Dispersion trading - subset portfolio

- Section: 6.3.1
- Asset class: Indexes
- Harness status: **not testable: options chains** - dispersion trading on a subset portfolio; needs options.

## Description (paper)

For some indexes, some component stocks may not have single-stock options. Often

these would be less liquid, lower market cap stocks. They would have to be excluded

113 Note that the pair-wise correlations ρ ij, i ̸ = j, typically are unstable out-of-sample, which can introduce a sizable error into this computation.

from the bought portfolio. Reducing the number of bought underlying single-stock options is also desirable to reduce transaction costs. Furthermore, the sample correlation matrix ρ ij is singular for a typical lookback period (e.g., daily close-to-close returns, going back 1 year, which is about 252 trading days) as the number of assets is large (500 for S&P 500 and even larger for other indexes). As mentioned above, the pair-wise correlations are unstable out-of-sample, which increases errors in the theoretical value σ I computed via Eq. (423). This can be mitigated as follows. 117

The singular and unstable correlation matrix can be made nonsingular and more stable by replacing it with a statistical risk model \[Kakushadze and Yu, 2017a\]. Let ( *A)

*i be the principal components of ρ ij with the eigenvalues λ ( *A) in the decreasing order, λ (1) \> λ (2) \> λ ( *r), where r is the rank of ρ ij (if r \< N, the other eigenvalues are null: λ ( *A) = 0, A \> r). The statistical risk model correlation matrix is given by $$ \psiij = \xi2 $$ i \deltaij +

K X

A=1

( A ) V ( A ) *i ( *A) *j (425) $$ i = 1 − $$

K X

A=1 ( *A) h

( A ) *i (426)

where K \< r is the number of risk factors based on the first K principal components that are chosen to explain systematic risk, and ξ i is the specific (a.k.a. idiosyncratic) risk. The simplest way to fix K is via eRank (effective rank) \[Roy and Vetterli, 2007\] - see \[Kakushadze and Yu, 2017a\] for details and complete source code for constructing ψ ij and fixing K. So, now we can use ψ ij (instead of ρ ij) to compute the theoretical volatility σ I:

I =

N X $$ i,j=1 $$ wiwj\sigmai\sigmaj\psiij =

N X $$ i=1 $$ i \sigma2 i \xi2 *i +

K X

A=1

" N X $$ i=1 $$

( A ) V ( A ) *i i\sigmai

2 (427)

The first term on the r.h.s. of Eq. (427) is due to the specific risk. The long portfolio then contains only the straddles corresponding to the first N ∗ single-stock options with the lowest N ∗ values of w 2 i \sigma2 i \xi2

*i. E.g., for S&P 500 we can take N ∗ = 100.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 6.3.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

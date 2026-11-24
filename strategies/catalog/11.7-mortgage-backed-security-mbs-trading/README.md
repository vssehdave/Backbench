# 11.7 Mortgage-backed security (MBS) trading

- Section: 11.7
- Asset class: Structured assets
- Harness status: **not testable: bonds/rates** - needs credit tranche, CDS or MBS data.

## Description (paper)

This strategy amounts to buying MBS passthroughs 182 and duration-hedging their interest rate exposure with interest rate swaps. Thus, the main risk of a passthrough MBS is the prepayment risk, whereby homeowners have an option to prepay their mortgages. Homeowners refinance their mortgages as the interest rates drop, which results in negative convexity in the MBS price as a function of the interest rates

180 In this case, for an upward-sloping curve, a flattener (steepener) has positive (negative) carry as S long \> S short ( *S long \< S short).

182 An MBS is an asset backed by a pool of mortgages. In a passthrough MBS, which is the most common MBS type, cash flows are passed from debtors to investors through an intermediary.

(e.g., the 5-year swap rate). The hedge ratios are model-dependent and a variety of

prepayment models can be constructed. Alternatively one can follow a nonparametric approach whereby using historical data one estimates the first derivative of the passthrough MBS price P w.r.t. the 5-year swap rate R with the constraint that *P is a non-increasing function of R (see, e.g., \[Duarte, Longstaffand Yu, 2006\]), 183

employing, e.g., a constrained regression (see, e.g., \[A¨ıt-Sahalia and Duarte, 2003\]).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 11.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

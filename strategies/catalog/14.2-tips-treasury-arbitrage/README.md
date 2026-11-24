# 14.2 TIPS-Treasury arbitrage

- Section: 14.2
- Asset class: Miscellaneous assets
- Harness status: **not testable: other data not available** - needs swap, TIPS, weather or energy data.

## Description (paper)

This strategy is based on the empirical observation that Treasury bonds tend to be overvalued relative to TIPS 195 almost all the time (see, e.g., \[Campbell, Shiller and Viceira, 2009\], \[Driessen, Nijman and Simon, 2017\], \[Fleckenstein, 2012\], \[Haubrich,

Pennacchi and Ritchken, 2012\]). The strategy amounts to selling a Treasury bond (whose price is P Treasury, fixed coupon rate is r Treasury, and maturity is T) and offsetting this short position with a synthetic portfolio, which precisely replicates the Treasury bond coupon and principal payments, but costs less than the Treasury bond. This synthetic portfolio is constructed by buying TIPS (whose price is P TIPS and maturity T is the same as that of the Treasury bond) with a fixed coupon rate r and n coupon payments at times t i, i = 1 ,..., n (with t n = T), and simultaneously selling n zero-coupon inflation swaps with maturities t i, the fixed rate K, and the notionals Ni = r + \deltati,T per $1 of the TIPS principal. The cash flows (per $1 notional) at t = t i are given by (as above, I ( *t) is the CPI value at time t; also, time is measured in the units of the (typically, semiannual) compounding periods):

$$ CTIPS(ti) = Ni I(ti)/I(0) $$ (504) Cswap(ti) = Ni 

(1 + K) *t i − I ( *t i) */I (0)  (505)

Ctotal(ti) = Cswap(ti) + CTIPS(ti) = Ni (1 + K)ti (506)

So, the synthetic portfolio converts the indexed payments from TIPS into fixed payments with the effective coupon rates r eff ( *t i) = r (1 + K) *t i. These synthetic coupon payments almost replicate the Treasury bond coupons r Treasury. The exact matching involves small long or short positions in STRIPS 196, which are given by (see, e.g., \[Fleckenstein, Longstaffand Lustig, 2013\] for details) $$ S(ti) = D(ti) $$ 

\[ *r Treasury − r eff ( *t i)\] + δ t i ,T  1 − (1 + K) *t i  (507)

where D ( *τ) is the value of the STRIPS with maturity τ at time t = 0 (i.e., D ( *τ) is a discount factor). In Eq. (507) the second term in the curly brackets (which is proportional to δ t i ,T and is nonzero only for i = n, i.e., at maturity T) is included as we must also match the principals at maturity. Note that the STRIPS positions are established at t = 0. The net cash flow C (0) at t = 0 is given by (note that the net cash flows at t \> 0 are all null by replication)

*C (0) = P Treasury − P TIPS − n X $$ i=1 $$ *S ( *t i) (508)

Empirically C (0) tends to be positive (even after transaction costs). Hence arbitrage.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 14.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

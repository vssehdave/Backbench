# 14.1 Inflation hedging - inflation swaps

- Section: 14.1
- Asset class: Miscellaneous assets
- Harness status: **not testable: other data not available** - needs swap, TIPS, weather or energy data.

## Description (paper)

This strategy amounts to buying (selling) inflation swaps in order to exchange a fixed (floating) rate of inflation for a floating (fixed) rate. Inflation swaps conceptually are similar to interest rate swaps (see Subsection 5.1.4). A buyer (seller) of an inflation swap is long (short) the inflation and receives the floating (fixed) rate. The buyer has a positive return if the inflation exceeds the expected inflation (i.e., the swap

fixed rate, a.k.a. the "breakeven rate"). The fixed rate typically is calculated as the interest rate spread between the Treasury notes/bonds (as applicable) and Treasury Inflation-Protected Securities (TIPS) with the same maturity as that of the swap. The floating rate usually is based on an inflation index such as the Consumer Price Index (CPI). The most common type of inflation swap is the zero-coupon inflation swap (ZC), which has only one cash flow at maturity T (measured in years). This cash flow is the difference between the fixed rate cash flow C fixed and the floating rate cash flow Cfloating. These cash flows, per $1 notational, are given by:

$$ Cfixed = (1 + K)T −1 $$ (500) Cfloating = I(T)/I(0) −1 (501)

Here: K is the fixed rate; and I ( *t) is the CPI value at time t ( *t = 0 is the time at which the swap contract is entered into). Another type of inflation swaps is the year-on-year inflation swap (YoY), which references annual inflation (as opposed to the cumulative inflation referenced by the zero-coupon swap). Thus, assuming for simplicity annual payments, we have (here t = 1 ,..., T is measured in years): 194

Cfixed(t) = K (502) Cfloating(t) = I(t)/I(t −1) −1 (503)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 14.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

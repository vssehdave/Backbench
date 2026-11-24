# 8.1 Moving averages with HP filter

- Section: 8.1
- Asset class: Foreign exchange
- Harness status: **not testable: FX** - needs FX spot or forward data; the alpaca and kraken data kinds do not provide it.

## Description (paper)

In Subsection 3.12 we discussed a trading strategy for stocks wherein the trading signal is based on 2 intersecting (shorter and longer) moving averages. A similar approach can be applied to FX as well. However, FX spot rate time series tend to be rather noisy, which can lead to false signals based on moving averages. To mitigate this, before computing the moving averages, the higher-frequency noise can first be filtered out, e.g., using the so-called Hodrick-Prescott (HP) filter. 140 Then, the remaining lower-frequency trend component (as opposed to the raw spot rate) can be used to compute the moving averages and generate the trading signal (see, e.g., \[Harris and Yilmaz, 2009\]). The HP filter is given by: $$ S(t) = S∗(t) + \nu(t) $$ (437) $$ g = $$

T X $$ t=1 $$ [S(t) −S∗(t)]2 + λ

T − 1 X $$ t=2 $$

\[ *S ∗ ( *t + 1) − 2 *S ∗ ( *t) + S ∗ ( *t − 1)\] 2 (438) *g → min (439)

Here: the objective function g is minimized w.r.t. the set of T values of S ∗ ( *t), t = 1 ,..., T; S ( *t) is the FX spot rate at time t; S ∗ ( *t) is the lower-frequency ("regular") component; ν ( *t) is the higher-frequency ("irregular") component, which is treated as noise; the first term in Eq. (438) minimizes the noise, while the second term (based on the discretized second derivative of S ∗ ( *t)) penalizes the variation in S ∗ ( *t); and λ is the smoothing parameter. There is no "fundamental" method to fix λ. Sometimes (but not always) it is set to λ = 100 *× n 2, where n is the data frequency measured on

an annual basis (see, e.g., \[Baxter and King, 1999\] for more detail). So, for monthly data, which is what is usually used in this context, n = 12. The estimation period usually spans several years (of monthly data). Once S ∗ ( *t) is determined, two moving averages MA( *T 1 ) and MA( *T 2 ), T 1 \< T 2, are calculated based on S ∗ ( *t). Then, as before, MA( *T 1 ) \> MA( *T 2 ) is a buy signal, and MA( *T 1 ) \< MA( *T 2 ) is a sell signal.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

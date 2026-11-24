# 15.3.1 Distress risk puzzle - risk management

- Section: 15.3.1
- Asset class: Distressed assets
- Harness status: **not testable: not a market trading rule** - distressed-debt investing needing bond and legal-process data, not a price rule.

## Description (paper)

This strategy is a variation of the distress risk puzzle strategy in Subsection 15.3. Empirical studies suggest that zero-cost healthy-minus-distressed (HMD) strategies tend to have a high time-varying market beta, which turns significantly negative following market downturns (usually associated with increased volatility), which can cause large losses if the market bounces abruptly (see, e.g., \[Garlappi and Yan, 2011\], \[O'Doherty, 2012\], \[Opp, 2017\]). This is similar to what happens in other

factor-based strategies. 202 To mitigate this, the strategy can be modified as follows (see, e.g., \[Eisdorfer and Misirli, 2015\]): HMD *∗ = σ target b\sigma HMD (519)

Here: HMD is for the standard HMD strategy in Subsection 15.3; σ target is the level of target volatility (typically, between 10% and 15%, depending on the trader preferences); and b *σ is the estimated realized volatility over the prior year using daily data. So, 100% of the investment is allocated only if b *σ = σ target, and a lower amount is allocated when b *σ \> σ target. When b *σ \< σ target, the strategy could be leveraged. 203

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 15.3.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

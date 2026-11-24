# 7.4.1 Volatility risk premium with Gamma hedging

- Section: 7.4.1
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

The ATM straddles in the above strategy are Delta-neutral. 135 So, this is a "Vega play", i.e., the trader is shorting Vega. If the underlying (S&P 500) moves, the short straddle is no longer Delta-neutral: if the underlying goes up (down), Delta becomes negative (positive). So a variation of this strategy is to use Gamma hedging to keep the strategy close to Delta-neutral, which is achieved by buying (selling) the underlying if it moves up (down). Then this becomes a "Theta play", i.e., the

135 Some of the Greeks for options are: Θ = ∂V/∂t (Theta), ∆= ∂V/∂S (Delta), Γ = \partial2V/\partialS2

(Gamma), ν = ∂V/∂σ (Vega). Here: V is the value of the option; t is time; S is the price of the underlying; σ is the implied volatility.

strategy now aims to capitalize on the Theta-decay of the value of the sold options. So, the price of this is the cost of the Gamma hedging, which reduces the P&L. As the underlying moves more and more away from the strike of the sold put and call options, the Gamma hedge becomes more and more expensive and eventually will exceed the collected option premia, at which point the strategy starts losing money.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.4.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

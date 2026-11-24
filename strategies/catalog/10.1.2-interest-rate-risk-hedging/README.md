# 10.1.2 Interest rate risk hedging

- Section: 10.1.2
- Asset class: Futures
- Harness status: **not testable: futures** - needs futures data and positions.

## Description (paper)

Fixed-income assets are sensitive to interest rate variations (see Section 5) and futures contracts can be used to hedge the interest rate risk. A long (short) hedge position amounts to buying (selling) interest rate futures in order to hedge against an increase (decrease) in the price of the underlying asset, i.e., a decrease (increase) in the interest rates. 162 The corresponding P&L ( *P L ( *t, T) for the long hedge and *P S ( *t, T) for the short hedge, assuming the position is established at t = 0 with the unit hedge ratio and the maturity is T) is given by:

PL(t, T) = B(0, T) −B(t, T)

(464) PS(t, T) = B(t, T) −B(0, T) (465) B(t, T) = S(t) −F(t, T) (466)

where B ( t, T ) is the futures basis. In practice, the hedge ratio may not be 1. If a

hedge is against a bond in the futures delivery basket, 163 then the conversion factor model 164 is commonly used to compute the hedge ratio h C:

h C = C M B

F

(467)

where M B is the nominal value of the bond, M F is the nominal value of the futures,

and C is the conversion factor. Unlike the conversion factor model, the modified duration hedge ratio h D can be used for both deliverable and non-deliverable bonds:

hD = \\beta DB

F

(468)

where D B is the dollar duration 165 of the bond, D F is the dollar duration of the

futures, and β (which is often set to 1) is the change in the bond yield relative to the change in the futures yield, both taken for a given change in the risk-free rate. 166

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 10.1.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

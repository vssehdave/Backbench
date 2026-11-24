# 5.15 Swap-spread arbitrage

- Section: 5.15
- Asset class: Fixed income
- Harness status: **not testable: bonds/rates** - needs bond, yield-curve or swap data and positions; the harness trades one daily equity or BTC series.

## Description (paper)

This dollar-neutral strategy consists of a long (short) position in an interest rate swap (see Subsection 5.1.4) and a short (long) position in a Treasury bond (with the constant yield Y Treasury) with the same maturity as the swap. A long (short) swap involves receiving (making) fixed rate r swap coupon payments in exchange for making (receiving) variable rate coupon payments at LIBOR (the London Interbank Offer Rate) L ( *t). The short (long) position in the Treasury bond generates (is financed at) the "repo rate" (the discount rate at which the central bank repurchases government securities from commercial banks) r ( *t) in a margin account. The per-dollar-invested rate C ( *t) at which this strategy generates P&L is given by

$$ C(t) = \pm[C1 −C2(t)] $$ (418) *C 1 = r swap − Y Treasury (419) $$ C2(t) = L(t) −r(t) $$ (420)

where the plus (minus) sign corresponds to the long (short) swap strategy. The long (short) swap strategy is profitable if LIBOR falls (rises). So, this is a LIBOR bet. 105

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.15. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

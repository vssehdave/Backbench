# 11.6 CDOs - curve trades

- Section: 11.6
- Asset class: Structured assets
- Harness status: **not testable: bonds/rates** - needs credit tranche, CDS or MBS data.

## Description (paper)

As in the case of bonds (see Subsection 5.13), a flattener (steepener) curve trade involves a simultaneous sale (purchase) of a short-term tranche and a purchase (sale) of a long-term tranche. Put differently, with a flattener (steepener), the trader is buying (selling) short-term protection and selling (buying) long-term protection, i.e., the trader expects the spread curve to flatten (steepen), whereby the spread between the long-term and short-term tranches decreases (increases). The carry of the curve trade over the period from time t to time t + ∆ *t can be defined as follows

*C ( *t, t + ∆ *t) = ( *M long S long − M short S short) ∆ *t (490)

where M long and M short are the long and short tranche notionals, and S long and S short are the corresponding spreads. The trade can be structured to be dollar-neutral (i.e., notional-neutral, M long = M short), 180 risky-duration-neutral ( *D long = D short, see Eq. (486)), carry-neutral ( *M long S long = M short S short), etc. 181 The P&L of the strategy is given by ( *M long and M short are the long and short tranche MTMs, see Eq. (485)): P&L = M long −M short (491)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 11.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

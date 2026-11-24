# 8.5 FX triangular arbitrage

- Section: 8.5
- Asset class: Foreign exchange
- Harness status: **not testable: FX** - needs FX spot or forward data; the alpaca and kraken data kinds do not provide it.

## Description (paper)

This strategy is based on 3 currency pairs. 150 Let these currencies be A, B and C. Then we have 2 chains: i) exchange A for B, exchange B for C, and exchange C for A; and ii) exchange A for C, exchange C for B, and exchange B for A. We will focus on the first chain as the second one is obtained by swapping B for C. Each currency pair has the bid and the ask; e.g., Bid ( *A → B) and Ask ( *B → A) for the A-B pair. So, the rate at which A is exchanged into B is Bid ( *A → B), while the rate at which B is exchanged into A is 1 */Ask ( *B → A). Therefore, Bid ( *B → A) = 1 */Ask ( *B → A), and Ask ( *A → B) = 1 */Bid ( *A → B). In the chain i) above, the trader starts with A and loops back to A with the overall exchange rate

$$ R(A \toB \toC \toA) = Bid(A \toB) \times Bid(B \toC) \times $$ *Ask ( *C → A) (453)

If this quantity is greater than 1, then the trader makes a profit. Such opportunities are ephemeral, so fast market data and trade execution systems are critical here. 151

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

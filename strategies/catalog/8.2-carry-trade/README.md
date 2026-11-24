# 8.2 Carry trade

- Section: 8.2
- Asset class: Foreign exchange
- Harness status: **not testable: FX** - needs FX spot or forward data; the alpaca and kraken data kinds do not provide it.

## Description (paper)

Pursuant to "Uncovered Interest Rate Parity" (UIRP), excess interest earned in one country compared with another country due to a differential between risk-free interest rates in these countries would be precisely offset by depreciation in the FX rate between their currencies: $$ (1 + rd) = Et(S(t + T)) $$ *S ( *t) (1 + r f) (440)

Here: r d is the domestic interest rate; r f is the foreign interest rate; both r d and r f are assumed to be constant over the compounding period T; S ( *t) is the spot FX rate at time t, which is the worth of 1 unit of the foreign currency in units of the domestic currency; and E t ( *S ( *t + T)) is the future (at time t + T) spot FX rate expected at time t. 141 UIRP does not always hold, giving rise to trading opportunities - which are not risk-free arbitrage opportunities (see below). Thus, UIRP implies that high interest rate currencies should depreciate w.r.t. low interest rate currencies, whereas empirically on average the opposite tends to transpire, i.e., such currencies tend to appreciate (somewhat). 142 So, the basic carry strategy amounts to writing (i.e., selling) forwards on currencies that are at a forward premium, i.e., the forward FX rate F ( *t, T) exceeds the spot FX rate S ( *t), and buying forwards on currencies that are at a forward discount, i.e., the forward FX rate F ( *t, T) is lower than the spot FX rate S ( *t). 143 The forward FX rate is given by 144 $$ F(t, T) = S(t) 1 + rd $$ 1 + r f (441)

141 Thus, 1 USD invested at time t in a risk-free asset in the U.S. would be forth (1+ *r d) USD at time t + T. Alternatively, 1 USD would buy 1 */S ( *t) JPY at time t, which sum could be invested in a risk-free asset in Japan at time t, which would be worth (1 */S ( *t)) × (1 + r f) JPY at time t + T, which in turn could be expected to be exchanged for ( *E t ( *S ( *t + T)) */S ( *t)) × (1 + r f) USD at time *t + T. Requiring that the U.S. and Japan investments yield the same return gives Eq. (440).

As mentioned above, the carry strategy 145 is not without risks: this trade can generate losses if the borrowed (lent) currency suddenly appreciates (depreciates) w.r.t. its counterpart, i.e., it is exposed to the FX rate risk. On the other hand, if we borrow the low interest rate currency with the maturity date T, invest the funds in the high interest rate currency, and hedge this position with a forward contract to exchange the high interest rate currency for the low interest rate currency at maturity T (so we can cover the loan), ignoring the transaction costs (and other subtleties such as taxes, etc.), this is a risk-free position and any gains therefrom would amount to risk-free arbitrage. Hence Eq. (441), which is a no-risk-free-arbitrage condition. 146

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# 7.2 VIX futures basis trading

- Section: 7.2
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

This is essentially a mean-reversion strategy. It is rooted in empirical observations (see, e.g., \[Mixon, 2007\], \[Nossman and Wilhelmsson, 2009\], \[Simon and Campasano, 2014\]) 126 that the VIX futures basis (defined below) has essentially no forecasting power for subsequent VIX changes but has substantial forecasting power for subsequent VIX futures price changes. The VIX futures basis B V IX (for our purposes here) is defined as

B V IX = P UX 1 − P V IX (429)

D = B V IX

T (430)

Here: P UX 1 is the price of the first-month contract VIX futures; 127 P V IX is the VIX price; D is the daily roll value; and T is the number of business days until the settlement (which is assumed to be at least 10). Empirically, the futures prices tend to fall for positive basis and rise for negative basis (mean-reversion). So, the strategy amounts to shorting VIX futures when the VIX futures curve is upwardsloping (a.k.a. "contango", so the basis is positive), and buying VIX futures when the VIX futures curve is downward-sloping (a.k.a. "backwardation", so the basis is negative). Here is a simple trading rule (see, e.g., \[Simon and Campasano, 2014\]): Rule =         

Open long UX1 position if D < −0.10 Close long UX1 position if D > −0.05 Open short UX1 position if D > 0.10 Close short UX1 position if D < 0.05 (431)

A short (long) UX1 position is exposed to a risk of a sudden increase (decrease) in the volatility, which typically occurs during equity market sell-offs (rallies), so this risk can be hedged by, e.g., shorting (buying) mini-S&P 500 futures. 128 The hedge

\[Dupire, 1994\], \[Glasserman and Wu, 2010\], \[He, Hsu and Rue, 2015\], \[Lamoureux and Lastrapes, 1993\], \[Mayhew, 1995\], \[Skiadopoulos, Hodges and Clewlow, 1999\]. 124 See, e.g., \[¨Aij¨o, 2008\], \[Corrado and Miller, 2005\], \[Fleming, Ostdiek and Whaley, 1995\], \[Maghrebi, Kim and Nishina, 2007\], \[Shaikh and Padhi, 2015\], \[Siriopoulos and Fassas, 2009\], \[Skiadopoulos, 2004\], \[Whaley, 2000\], \[Whaley, 2009\].

125 E.g., RVX (CBOE Russell 2000 Volatility Index), VXEEM (CBOE Emerging Markets ETF Volatility Index), TYVIX (CBOE/CBOT 10-year U.S. Treasury Note Volatility Index), GVZ (CBOE Gold ETF Volatility Index), EUVIX (CBOE/CME FX Euro Volatility Index), VXGOG (CBOE Equity VIX on Google), VVIX (CBOE VIX of VIX Index), etc.

ratio can be estimated, e.g., based on a historical serial regression of the VIX futures price changes over the front-month mini-S&P 500 futures contract returns. 129

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

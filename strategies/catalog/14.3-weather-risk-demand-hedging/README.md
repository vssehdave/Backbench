# 14.3 Weather risk - demand hedging

- Section: 14.3
- Asset class: Miscellaneous assets
- Harness status: **not testable: other data not available** - needs swap, TIPS, weather or energy data.

## Description (paper)

Various businesses and sectors of the economy can be affected by weather conditions, both directly and indirectly. Weather risk is hedged using weather derivatives. There are no "tradable" weather indexes, so various synthetic indexes have been created.

196 STRIPS = "Separate Trading of Registered Interest and Principal of Securities". Essentially, STRIPS are zero-coupon discount bonds.

The most common ones are based on temperature. The cooling-degree-days (CDD)

and heating-degree-days (HDD) measure extreme high temperatures and extreme low temperatures, respectively: 197

I CDD = *n X $$ i=1 $$

max(0, T i − T base ) (509)

I HDD = *n X $$ i=1 $$

max(0, T base − T i ) (510)

T i = T min

Here: i = 1,..., n labels days; n is the life of the contract (a week, a month

or a season) measured in days; T min i and T max*

i

are the minimum and maximum temperatures recorded on the day labeled by i; and T base = 65 *◦ F. Then, the demand risk for heating days can, e.g., be hedged by a short futures position or a long put option position with the hedge ratios given by (here (Cov) Var is serial (co)variance):

HDD

futures = Cov( q w, I HDD ) / Var( I HDD ) (512)

HDD

put

= −Cov (qw, max(K −IHDD, 0)) /Var (max(K −IHDD, 0)) (513)

Here: q w is the portion of the demand affected by weather conditions (as there might

be other, exogenous, non-weather-related components to the demand); and K is the strike price. Similarly, the demand risk for cooling days can, e.g., be hedged by a long futures position or a long call option position with the hedge ratios given by:

CDD

futures = Cov( q w, I CDD ) / Var( I CDD ) (514)

CDD

call

= Cov (qw, max(ICDD −K, 0)) /Var (max(ICDD −K, 0)) (515)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 14.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

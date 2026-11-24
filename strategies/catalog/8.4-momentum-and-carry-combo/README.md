# 8.4 Momentum & carry combo

- Section: 8.4
- Asset class: Foreign exchange
- Harness status: **not testable: FX** - needs FX spot or forward data; the alpaca and kraken data kinds do not provide it.

## Description (paper)

This is a combination of the momentum strategy (Subsection 8.1) 149 and the carry strategy (Subsection 8.2), or their variations. There is a variety of ways these strategies can be combined (including an equally weighted combo, or some ideas discussed in, e.g., Subsection 3.6 and Subsection 4.6). A simple combination is based on minimizing the variance of the combo strategy using the sample covariance matrix of historical returns R 1 ( *t s) and R 2 ( *t s) of the two strategies (see, e.g., \[Olszweski and Zhou, 2013\]). Let (here Var and Cor are serial variance and correlation, respectively) $$ 1 = Var(R1(ts)) $$ (445)

$$ 2 = Var(R2(ts)) $$ (446) $$ \rho = Cor(R1(ts), R2(ts)) $$ (447)

Then minimizing the historical variance of the combined return R ( *t s) fixes the strategy weights w 1 and w 2:

$$ R(ts) = w1 R1(ts) + w2 R2(ts) $$ (448) $$ w1 + w2 = 1 $$ (449) Var( *R ( *t s)) → min (450) $$ w1 = $$ 2 −\sigma1\sigma2\rho 1 + \sigma2 2 −2\sigma1\sigma2\rho (451) $$ w2 = $$ 1 −\sigma1\sigma2\rho 1 + \sigma2 2 −2\sigma1\sigma2\rho (452)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

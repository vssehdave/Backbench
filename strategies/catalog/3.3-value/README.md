# 3.3 Value

- Section: 3.3
- Asset class: Stocks
- Harness status: **not testable: data not available** - Alpaca has no fundamentals (book value, earnings), only prices; the strategy ranks stocks by book-to-price. A price-only stand-in would be a different strategy, so none is run.

## Description (paper)

This strategy amounts to buying winners and selling losers as in the price-momentum and earnings-momentum strategies, but the selection criterion is based on value. Value can be defined as the Book-to-Price (B/P) ratio (see, e.g., \[Rosenberg, Reid and Lanstein, 1985\]). Here "Book" is the company's book value per share outstand- ing (so the B/P ratio is the same as the Book-to-Market ratio, where now "Book" stands for its total book value, not per share outstanding, and "Market" is its market capitalization). The trader can, e.g., construct a zero-cost portfolio by buying stocks in the top decile by the B/P ratio, and shorting stocks in the bottom decile. There can be variations in the definition of the B/P ratio. Thus, e.g., \[Asness, Moskowitz and Pedersen, 2013\] uses current (i.e., most up-to-date) prices, while \[Fama and French, 1992\] and some others use prices contemporaneous with the book value. 43

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

# 6.5 Index volatility targeting with risk-free asset

- Section: 6.5
- Asset class: Indexes
- Harness status: **tested**. Rule as implemented: Weight = target volatility / 20-day realised volatility, capped at 1 and rounded down to quarter steps; the remainder is cash earning 0%. Target in {10%, 15%} is the author's choice. Approximation: the paper's kappa rebalance threshold needs state that decide() does not have.

## Description (paper)

A volatility targeting strategy aims to maintain a constant volatility level, which can be achieved by a periodic (weekly, monthly, etc.) rebalancing between a risky asset - in this case an index - and a riskless asset (e.g., U.S. Treasury bills). 119 If σ is the volatility of the risky asset 120 and the volatility target is σ ∗, then the allocation weight for the risky asset is given by 121 w = σ ∗ /σ, and the allocation weight for the risk-free asset is 1 − w. To avoid overtrading and reduce transaction costs, rebalancing (instead of periodically) can be done based, e.g., on a preset threshold *κ, say, only if the percentage change \| ∆ *w \| /w since the last rebalancing exceeds κ.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 6.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

Real data: SPY daily raw SIP bars from Alpaca, 2016-01-01 to 2026-01-01 (exclusive), run with `python money.py test 6.5-index-volatility-targeting-with-risk-free-asset/manifest.json --start 2016-01-01 --end 2026-01-01` (saved as `results.json`). Defaults: 20 stress paths, 10 bps shock, seed 42.

| Forward window | Selected | Strategy | Cash | Buy and hold | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0.15 | 2.76% | 0.00% | 3.39% | 3+1 |
| 2017-07-01..2018-01-01 | 0.1 | 5.19% | 0.00% | 5.28% | 2+1 |
| 2018-07-01..2019-01-01 | 0.1 | -0.21% | 0.00% | -3.51% | 2+4 |
| 2019-07-01..2020-01-01 | 0.15 | 4.05% | 0.00% | 4.77% | 3+2 |
| 2020-07-01..2021-01-01 | 0.1 | 4.17% | 0.00% | 9.69% | 10+5 |
| 2021-07-01..2022-01-01 | 0.15 | 4.16% | 0.00% | 5.98% | 3+3 |
| 2022-07-01..2023-01-01 | 0.1 | 0.43% | 0.00% | 0.58% | 7+5 |
| 2023-07-01..2024-01-01 | 0.15 | 3.48% | 0.00% | 4.20% | 2+1 |
| 2024-07-01..2025-01-01 | 0.15 | 2.73% | 0.00% | 4.03% | 4+3 |
| 2025-07-01..2026-01-01 | 0.1 | 3.53% | 0.00% | 5.23% | 7+5 |
| **Compounded** | | **34.61%** | 0.00% | 46.79% | |

Strategy ranks above buy and hold in 1 of 10 windows; abstentions 0. Cash and buy-and-hold are the repo's own `controls:cash` and `controls:buy_and_hold` run through the same folds, fees and sizing (`../_benchmarks/`).

Read with care:
- Only the second half of each calendar year (July-December) is a forward window; the other half trains. Ten windows cover half the decade, so the compounded numbers are not a ten-year return.
- Each window is one 6-month sample, and the level is chosen per window on a 3-month selection slice, so the selected level changes.
- Prices are raw (no dividends), which understates buy-and-hold and the long legs equally.
- Signals use the prior close and fill at the next open, with the repo's IBKR fee model; position is a fixed share count of about 5,000 USD at the window's first training close (half of the 10,000 USD of cash).
- Parameters are the paper's examples where it gives them, otherwise the author's fixed choice (see Harness status), and were not changed after seeing results.

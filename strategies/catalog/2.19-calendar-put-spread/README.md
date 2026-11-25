# 2.19 Calendar put spread

- Section: 2.19
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*1.0000 (next-next expiry, closed at the near expiry); short 1 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-10-16), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a horizontal spread consisting of a long position in a close to ATM put option with TTM T ′ and a short position in another put option with the same strike price *K but shorter TTM T \< T ′. This is a net debit trade. The trader's outlook is neutral to bearish. At the expiration of the short put option ( *t = T), the best case scenario is if the stock price is right at the strike price ( *S T = K). At t = T let V be the value of the long put option (expiring at t = T ′) assuming S T = K. We have:

*P max = V − D (75) *L max = D (76)

If at the expiration of the short put option the stock price K ≤ S T ≤ S stop − loss, where S stop − loss is the stop-loss price above which the trader would unwind the

entire position, then the trader can write another put option with the strike price *K and TTM T 1 \< T ′. While maintaining the long position in the put option with TTM T ′, the trader can generate income by periodically selling put options with shorter maturities. In this regard, this strategy resembles the covered put strategy.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.19. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-10-16, 33 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned. The far leg is closed at the near expiry, so the last monthly expiry is dropped (one cycle fewer).

| | Total return | Max drawdown |
|---|---|---|
| calendar put spread | 22.4% | -4.8% |
| SPY buy and hold | 56.2% | -18.5% |

Opened 32/33 cycles, ITM leg expiries 8, assignments 8, fees USD 124.80, missing-bar days 94, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: 22.8% / 21.8% / 20.9%.

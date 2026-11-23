# Historical U.S. equity ticks

Research decision recorded November 22, 2026. The first acquisition target is consolidated trades and top-of-book quotes for QQQ and TQQQ, starting with one session on January 4, 2016. Both streams matter. Trades can reconstruct VWAP, while quotes support spread-aware execution studies. A top-of-book history provides limited evidence about queue position, impact or guaranteed fills.

| Source | Evidence and applicable limits | Decision |
|---|---|---|
| Waterloo / WRDS / NYSE TAQ | Waterloo lists NYSE TAQ in its WRDS subscription. NYSE describes consolidated trades, quotes, NBBO and symbol master files covering 2016. Waterloo lists variable coverage and requires an account application. Personal entitlement and permitted uses remain unverified. | Potentially zero incremental data cost for eligible academic research. Confirm dataset, dates, usage, extraction limits and retention under the specific licence in Waterloo Omni. Class accounts require an instructor's code. |
| Massive Stocks Advanced | The individual plan lists US$199/month. The company reports listed stock trades and quotes dating to September 2003. Its ten-year Developer window rolls forward and excludes the beginning of 2016 as of the review date. Full-history quotes require Advanced. OTC coverage starts in December 2021. | Concrete paid candidate for personal research. Confirm the account qualifies and that the subscribed licence permits the intended use and retention. For the pilot take the per-symbol API path. |
| IBKR historical ticks | The TWS API documents three years of historical tick coverage, one trading session per request and a Level 1 subscription requirement. | Useful as a recent cross-check. A complete 2016 backfill needs another source. |

Sources: [Waterloo WRDS catalogue](https://subjectguides.uwaterloo.ca/az/wrds-wharton-research-data-services), [Waterloo electronic-resource guidelines](https://uwaterloo.ca/lib/find-resources/copyright/eresources-use-guidelines), [WRDS class accounts](https://wrds-www.wharton.upenn.edu/pages/about/wrds-account-types/student-guide-enrolling-in-a-class-account/), [NYSE Daily TAQ](https://www.nyse.com/data-products/catalog/daily-taq/), [Massive coverage](https://massive.com/knowledge-base/article/how-much-historical-stock-data-does-massive-have), [Massive quote plans](https://massive.com/docs/flat-files/stocks/quotes), [IBKR historical time and sales](https://www.interactivebrokers.com/docs/tws-api/doc/md/historical-ticks).

## Storage and coverage

Massive lists 143 GB of all-market trades and 571 GB of all-market quotes for 2016 alone. The combined 714 GB exceeds a 512 GB drive before any conversion or indexes. Begin with ticker/day partitions. Measure actual compressed bytes, requests, processing time and number of sessions before approving a larger range. Prices and sizes in stock flat files are as traded. Preserve the raw units and apply corporate actions in a separate derived series. [Trade archive](https://massive.com/docs/flat-files/stocks/trades) · [Quote archive](https://massive.com/docs/flat-files/stocks/quotes) · [Flat-file conventions](https://massive.com/docs/flat-files/stocks/overview)

Coverage is per security and listing lifetime. For example, a company first listed in 2020 has no 2016 tape. Query reference records as of the session date for changes of ticker, delistings and reused symbols. Record both requested and observed ranges. Distinguish an empty successful response, a market closure, a trading halt, a coverage gap and an entitlement denial.

## Acceptance of the first paid or institutionally entitled sample

1. Retain provenance, provider/feed, dataset type, instrument identity, timestamp fields, market date, timezone and nanosecond precision, conditions, exchange, sequence identifiers and correction indicators when supplied. Inspect actual 2016 field availability.
2. Check records across regular-session boundaries and preserve the unfiltered source separately from any regular-session analysis. Use the time the consolidated feed reported each event for simulated availability and model feed latency explicitly. Do not apply a retrospective correction before it was observable.
3. Reconstruct volume and VWAP using documented sale conditions. Check one session against an independent source using identical sessions, trade eligibility and units. Investigate discrepancies before extending the backfill. Independently compare bid/ask coverage and spreads.
4. Keep raw licensed feeds and credentials outside Git. Record an entitlement decision and budget before a paid run. No purchase or entitlement is implied by the public catalogue.

# Money | Multi-strategy trading platform
## Objective and deployment contract

Run several stock and crypto strategies simultaneously, keep a local audit trail, and notify the owner on Discord for every execution. Measure success in spendable CAD after costs, estimated incremental tax and both subscriptions. Show total equity alongside cash available for bills. The deliverable here is an implementation plan. No edge, execution permission or deployable balance is assumed.

Deploy every registered strategy version as a running paper worker. Give each a parallel live allocation setting from zero up to its approved risk budget. A failed strategy remains observable with zero live allocation. A funded strategy continues paper trading alongside live trading so execution divergence is measurable. If the goal is eventual funding for every strategy, report each one's unmet criteria individually. Funding all versions unconditionally conflicts with the profitability constraint.

## First release — standalone strategy testing framework

Build stages 1–3 as one locally runnable Qlib research product before implementing the candidate strategies below. Use deterministic fixtures to exercise the contract: a cash-only control, a threshold strategy with a known trade and a small fitted fixture for fold isolation. The fixtures have hand-checkable expected outcomes.

A plug-in supplies a versioned manifest, optional fit function and decision function. Declare required fields, universe, calendar, lookback, label horizon, tunable parameters, benchmark and supported execution assumptions. Fit receives only the current training partition. Decide receives the available history and current portfolio state and returns targets or an explicit abstention. The harness owns the clock, fold boundaries, simulated execution, ledger, metrics and random seeds. Discover each plug-in from its manifest. Validate missing fields, incompatible calendars and unsupported order types before a run begins.

Proposed local CLI:
- `money test --strategy threshold_fixture --suite full --scenario us_equities` runs baseline replay, sensitivity and regime analysis, rolling 6+6 evaluation and seeded perturbation Monte Carlo.
- `money compare RUN_A RUN_B` displays benchmark-relative net CAD return, drawdown, turnover, fees, worst forward window, regime breakdown and Monte Carlo downside. Summarize skipped trades and sample sizes. Flag differences in period, universe, capital, cost model and benchmark. Allow a matched rerun using a shared configuration.
- `money replay RUN_ID --path PATH_ID` reconstructs a specified perturbation and its decisions from the saved manifest.

Persist machine-readable manifests, fold metrics, timestamped signals, orders, fills, equity curves and scenario summaries along with a human-readable comparison. Record code and plug-in version, data snapshot, resolved parameters, calendars, costs and seeds. Flag unavailable metrics and failed runs explicitly.

Release acceptance: add a previously unseen fixture package using its manifest alone, then run and compare it against the control without editing the runner. Check results against hand-calculated cash and fees. Verify time isolation, deterministic reruns, within-window portfolio accounting, parameter fragility detection and a perturbation that changes an actual order. Run the complete suite on stock and crypto calendars from a clean setup without broker credentials or Discord. Only then begin production strategy development.

## Initial strategy catalogue

Start with unlevered, long/cash strategies. The numbers below are hypotheses to register before evaluation, not optimized parameters. Use the next eligible tradable quote after signal availability.

| ID | Decision and exit | Parameters and comparator |
|---|---|---|
| EQ1 • Relative momentum | Monthly, rank a point-in-time liquid US equity universe by trailing six-month total return excluding the newest month. Buy the leading quintile in equal weights and sell names that leave it. | Vary lookback, skipped period, rank cutoff and turnover buffer. Compare with equal-weight universe and broad US total return in CAD. |
| EQ2 • Management claims | Extract dated, quantified guidance or operating claims by metric, segment and period from releases, filings or licensed transcripts. Buy on a newly corroborated improvement, exit on contradiction, expiry after 20 sessions, or withdrawal. Retain bearish observations in the long/cash book. | Vary evidence threshold, holding horizon and publication delay. Compare with sector peers over identical event windows and a simpler earnings-change rule. |
| EQ3 • Insider buying | On public disclosure of discretionary open-market purchases by two distinct officers/directors within 30 days, enter at the next eligible session. Exit after 40 sessions. Deduplicate amendments and exclude grants and option exercises. | Vary cluster size, significance relative to holdings, and holding period. Compare with matched sector/size peers. |
| CR1 • BTC trend | On a completed UTC daily bar, hold BTC when a fast moving average exceeds a slow average, otherwise CAD. Start with 20/80 days. | Vary both lookbacks and a trading buffer. Compare with BTC buy-and-hold and a cash/BTC mix with similar volatility. |
| CR2 • ETH short-term reversal | In a positive trailing 60-day trend, buy ETH after a daily return below its trailing 60-day tenth percentile. Exit on recovery to the preceding close or after three days. | Vary percentile, trend filter and expiry. Compare with ETH at matched average exposure. |
| CR3 • BTC/ETH relative strength | Weekly, hold the stronger coin by trailing 30-day CAD return if positive, otherwise hold CAD. Switch only when the return gap exceeds a predeclared buffer. | Vary lookback, switch threshold and rebalance day. Compare with a regularly rebalanced 50/50 BTC/ETH book. |

For EQ2, store verbatim evidence spans, source identifiers, observed and publication times, claim scope, confidence, and the reason two claims agree or conflict. Separate contradictions from changes in scope or new information. Deduplicate syndicated news. Institutional holdings and permitted political data can be tested as incremental features with disclosure lag and source-use rights recorded. Compare each addition against the original strategy. Mask tickers and future context where feasible when replaying documents through modern LLMs. Pretraining contamination cannot be eliminated by masking, so prospective evidence is especially important here.

## Qlib integration and data boundary

Use Microsoft's Qlib for research datasets, model fitting, experiment records and historical portfolio simulation. Pin Qlib, Python and the environment after a Windows compatibility smoke test. Keep calendar-specific data providers and jobs isolated for US exchange sessions and 24/7 UTC crypto. Start with daily data, selected event documents and decision-time quotes on the existing 16 GB CPU machine. Track runtime and disk use before adding intraday history.

Maintain immutable raw snapshots and normalized Parquet partitions. For each observation, retain effective time, publication time, first received time, revision, currency, instrument ID, venue and vendor. Include delisted equities and historical membership, splits, dividends, corporate actions, FX, outages and missing bars. Adjust signals consistently and simulate fills in tradable units. Reconcile adjusted-series returns against cash dividends and splits to avoid double counting. Imported archives lacking first-seen timestamps need a documented conservative availability rule and a separate quality flag.

A strategy package declares its identifier/version, data requirements, calendar, warm-up, cadence, prediction horizon, parameter space, costs, benchmark and exposure limits. Its optional fit step returns a versioned artifact. Its decision step consumes an as-of snapshot, positions and fitted state, and emits target exposure, expiry and evidence. The same decision function runs in research, replay, paper and live. Wrap it in Qlib BaseStrategy for portfolio simulation. Package learned models through Qlib dataset/model interfaces and record signals and metrics through the experiment recorder. Use an explicit calendar-month task generator for 6+6 folds. Qlib RollingGen advances by calendar-index steps, which differ by market. Custom adapters supply crypto lot sizes, continuous sessions, actual fees and fill assumptions. IBKR and the crypto venue are separate live adapters. Test new instruments, order types or frequencies against the simulator's supported capabilities before certifying their results.

## Validation specification

### 1. Parameter and regime sensitivity

Pre-register ranges, evaluation metrics and a trial budget per family. For each tunable numeric parameter try feasible local changes such as ±5%, ±10% and ±20%, rounding discrete values and retaining meaningful alternatives. Test interactions between important pairs. For a rule without fitted parameters, vary decision latency, fill price, fee tier and data availability. Evaluate the original rule and its neighbours on identical dates, universe, costs and capital. Publish the full surface, median neighbour return, share profitable, worst drawdown, counts and turnover. Prefer a stable region on training data and freeze its selection rule.

Tag regimes using trailing information at the decision time. Suggested axes are benchmark trend, realized volatility and liquidity/spread. Fit any quantile cutoffs only on the training fold. Report net return, benchmark-relative return, drawdown, exposure, number of independent events and time spent in each regime. Include transitions, such as a breakout strategy entering just before a reversal. Mark sparse regimes inconclusive. Distinguish a strategy designed to sit in cash in a downtrend from one that repeatedly loses while invested. Predeclare whether a regime is a reporting label or an actual deployment filter.

### 2. Six calendar months of optimization, six unseen months forward

| Fold | Optimize, including internal chronological validation | Freeze and forward-test |
|---|---|---|
| 1 | Jan–Jun 2022 | Jul–Dec 2022 |
| 2 | Jan–Jun 2023 | Jul–Dec 2023 |
| 3 | Jan–Jun 2024 | Jul–Dec 2024 |

Advance by twelve calendar months. Align stock decisions to their exchange sessions and crypto decisions to UTC boundaries. At each cutoff, select hyperparameters, models, feature processors, sizing and regime cutoffs using only the preceding six months with chronological inner splits. Purge samples whose outcome or holding interval overlaps validation/test boundaries and impose a gap appropriate to label availability. Earlier prices may warm up a rolling feature without contributing additional fitted examples. When six months contain too few independent events, report insufficient evidence. Avoid padding the sample with duplicated articles or overlapping trades.

Freeze the chosen artifact and replay forward one decision at a time. Start each independent forward simulation with equal capital and zero positions. Warm the strategy with its own training history and execute its signals from the first eligible forward open. Compare the in-sample and forward returns after fees and report buy and sell counts. Keep training and forward windows disjoint across all batches. Keep a sealed final historical block or a prospective paper period for the selected family. Once a researcher changes the design in response to forward results, record a new version and treat the reviewed period as development evidence. Log every discarded trial to expose selection bias.

### 3. Monte Carlo on strategy and portfolio

Every strategy must pass through a seeded perturbation replay in each held-out six-month fold. Start from the same opening state as its unperturbed replay. Perturb the inputs before decisions, rebuild derived features, and rerun the frozen strategy, portfolio allocator, order sizing, fills, costs and ledger through the end of each path. Carry each path’s state within its forward window and reset at the next independent batch. Use synchronized shocks across strategies competing for the same cash.

| Perturbation | Replay design |
|---|---|
| Market and regime | Apply volatility-scaled return shocks, gaps, volatility clusters and joint equity/crypto selloffs. Preserve coherent prices, cross-asset dependence, market hours and weekend reopening gaps. |
| Information | Delay or drop a filing, news event or price update. Recompute the signal and its expiry using only information available at the simulated instant. |
| Parameters | Draw bounded joint changes around the trained settings, respecting valid combinations and integer constraints. Freeze each draw for its fold and record it. Compare combined effects with the one-at-a-time sensitivity results. |
| Execution | Sample spreads, latency, liquidity, partial or rejected fills and outages conditional on the market state. Reconcile outstanding orders, available cash and risk limits before the next decision. |

Estimate perturbation ranges and dependencies from the training window or prior observations and lock them before forward testing. Report empirical scenarios separately from deliberately severe, hypothetical stresses. Run each family alone and in combination with paired seeds for attribution. Start with pilot batches and target 5,000 paths where computationally feasible. Check tail estimates across seeds and report their precision. A synchronized block bootstrap of realized out-of-sample returns provides a separate trade-sequence diagnostic.

Verification requires zero perturbation to reproduce the original orders, fills and equity curve. A seeded boundary test must change a signal or order when a price crosses its trigger, and a delayed-release test must suppress a trade whose signal expires. Record the seed, input snapshot, frozen model, draw and resulting trades so each case can be reproduced. Report how many simulated decisions changed, trades appeared or disappeared, and how much net CAD profit and drawdown changed relative to the paired baseline.

Report median and fifth-percentile ending CAD equity, 95th-percentile maximum drawdown, expected shortfall in the worst 5% of paths at a stated horizon, frequency of breaching the owner’s loss limit, fraction of months covering both bills, and longest shortfall streak. Show uncertainty for a one-year horizon with monthly bill withdrawals and tax-reserve updates. These are conditional scenario estimates. Sparse history and missing regimes limit their interpretation.

## Selection, funding and portfolio construction

Freeze numerical gates before viewing protected results. Owner supplies starting capital, maximum acceptable CAD loss/drawdown, desired cash buffer, monthly subscription bills and acceptable frequency of missed months. Report absolute P&L, benchmark-relative performance, turnover, estimated capacity at actual order sizes, worst fold, independent trade count and downside under high-cost execution. Assess strategy families jointly to account for multiple trials. Report uncertainty with dependence-aware intervals. A positive average without sufficient evidence goes to paper with zero live allocation.

Run every strategy alone, then replay the intended portfolio on one shared cash balance. Start from capped equal risk budgets with a cash floor. Map overlapping positions and factor exposures; CR1 and CR3 can both own BTC. Net compatible targets before routing, attribute fills and fees by a deterministic rule, cap exposure per instrument/asset class/venue, reserve for taxes and bills, and stress correlated losses. Run leave-one-strategy-out comparisons. Incremental portfolio contribution can justify a diversifier with a lower standalone return. Compare against cash and passive portfolios with similar exposure and the same withdrawal assumptions.

Deployment sequence per version: reproducible replay, continuously running paper, capped live pilot after owner authorization, then budget increases only after fill quality and risk match assumptions. Pause new entries on stale feeds, irreconcilable positions, violated loss limits or expired signals. Specify whether outstanding orders are cancelled and who manages exits during a pause. Never silently liquidate all positions on a routine disconnect.

## Runtime, reporting and accounting

One always-on local Windows host initially runs collectors, decision workers, a single order/risk service, IB Gateway, a SQLite ledger and Discord delivery. Give research jobs CPU and memory limits; schedule large simulations away from latency-sensitive work. Use encrypted backups on separate storage and test recovery. An external heartbeat detects total host failure. Evaluate a VPS or dedicated host by comparing its recurring costs with missed opportunity and reliability benefits. Budget for IB Gateway reauthentication. Keep venue keys local with minimal permissions, disable crypto withdrawal permissions on trading keys, and keep raw tax documents outside Discord.

Separate paper and live accounts. Persist a unique order intent and cash reservation before submitting. On ambiguous timeouts query venue state and reconcile before retrying. Ingest partial fills, cancellations, rejects, adjustments and transfers idempotently. Save notification jobs in the same transaction as fills. Ping the owner on every execution, including fills recovered after downtime, with mode, strategy, venue, quantity, price, fees and trade ID. Owner-only controls include status, positions, risk, pause and monthly results. Record the operator and every mode or allocation change.

Build the CAD ledger at inception. Preserve original amounts, fees, FX rate and source, trade/settlement times, deposits, withdrawals, dividends, withholding and corrections. Track shared costs, data, electricity/hosting, model APIs and both subscriptions once. Compute cash available for bills and total marked equity net of external cash flows. For taxes, reconcile all relevant holdings and opening balances, capital-account adjusted cost base and superficial losses where applicable, and business-account treatment where applicable. Keep a separate sports ledger and resolve the classification based on facts. Reserve estimated incremental tax using projected personal returns with and without the activity. Separate estimated, assessed and paid amounts; produce year-end schedules, exceptions and reconciliation to broker records. Filing and payment require the owner's authorization. Show a provisional flag when the tax inputs are incomplete.

Start equities with eligible US instruments through IBKR Canada and a verified account-specific commission/FX schedule. IBKR restrictions on automated Canadian-marketplace orders matter when expanding the universe. Evaluate Kraken spot for crypto. Confirm eligible Canadian pairs, trade permissions, account fee tier, minimum lots and actual execution charges. Paper-simulate sports arbitrage and positive-EV rules as an extension using separate odds and settlement adapters, including voids, sportsbook rules, stake limits, and one-leg failure. Seek an Ontario venue that permits the intended automated execution; Pinnacle invites API inquiries. Exclude prohibited cross-book arbitrage venues. Qlib supports the stock and crypto research layers; sports uses the common test/report contract with an event-settlement simulator.

## Delivery milestones and acceptance tests

| Stage | Build | Evidence required for completion |
|---|---|---|
| 1 • Foundation | Pin Qlib environment, ingest one equity and one crypto pair, create raw snapshots, calendars, manifests and ledger. | A clean replay from saved inputs reproduces a split-adjusted stock return and a weekend crypto decision. |
| 2 • Common harness | Implement the strategy interface, Qlib wrappers, realistic fee/fill adapters, fold generator and experiment registry. | A deliberately future-dated input is rejected. Changing future data cannot change a prior decision. Folds have exact six-month boundaries, disjoint forward observations and independent starting capital. |
| 3 • Validation | Implement parameter grids, regime attribution, seeded perturbation replays, joint block bootstrap and portfolio reports. | Fixed seeds reproduce path statistics. An intentionally brittle strategy is flagged. Simultaneous stock/crypto losses remain visible in the portfolio simulation. |
| 4 • Strategy deployment | Implement all six hypotheses and deploy six independent paper workers. Ingest source-specific records for the event strategies. | Every worker reports status, a data watermark, model version and explicit trade or abstention reason. Replay and paper decisions agree on identical inputs. |
| 5 • Operations and tax | Deliver Discord, backups, reserve tracking, statements and cost reports. | Replay a crash after submission, duplicate fill, lost Discord connection and backup restore. No duplicate order or ledger charge. Reconcile an example month through to CAD cash and ending equity. |
| 6 • Live rollout | Connect verified IBKR and crypto accounts and enable individually approved allocations. Evaluate sports venue access separately. | Each funded strategy has a sealed validation report, demonstrated operational recovery, owner-set loss limits and a reconciliation of live versus expected fills. |
| 7 • Ongoing review | Monthly cost/coverage report, drift tracking and scheduled six-month refits. | Archive every model, dataset, configuration and result. Revert by version while preserving open-position ownership and full history. |

Stages 1–3 together deliver the first release. Build the six candidate strategies only after the framework acceptance run passes. Discord, brokerage connections and continuously running workers follow in the deployment phases.

## Primary references

- [Microsoft Qlib](https://github.com/microsoft/qlib) · [Rolling task implementation](https://github.com/microsoft/qlib/blob/main/qlib/workflow/task/gen.py) · [Strategy interface](https://github.com/microsoft/qlib/blob/main/qlib/strategy/base.py)
- [IBKR Canada API restriction](https://www.interactivebrokers.com/support/faq/content/use-api-canada-73525898) · [IBKR commissions](https://www.interactivebrokers.ca/en/index.php?f=49637) · [IB Gateway operations](https://www.interactivebrokers.com/support/faq/content/ib-gateway-41571362)
- [Kraken Canada trading API](https://www.kraken.com/ca/pro/trading-api) · [Kraken Pro Canada fees](https://www.kraken.com/ca/pro/fees)
- [Pinnacle Canada API](https://www.pinnacle.ca/en/api) · [bet365 Ontario terms](https://help.on.bet365.ca/s/en-ca/terms-and-conditions) · [US House disclosure use restrictions](https://disclosures-clerk.house.gov/FinancialDisclosure/ViewSearch)
- [CRA securities reporting](https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/tax-slips/understand-your-tax-slips/t5-slips/t5008-statement-securities-transactions-slip-information-individuals.html) · [CRA crypto records](https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/compliance/cryptocurrency-guide/books-records-crypto.html) · [CRA gambling guidance, section 13.2.7](https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax-audit-manual-domestic-compliance-programs-branch-dcpb-13.html)

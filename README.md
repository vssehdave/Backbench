# Wallet research harness

Run from the repository root with Python 3.10 or later. The deterministic fixtures use the standard library. Each evaluation writes a JSON report to the specified path.

```sh
python -m unittest -v
python harness.py --strategy controls:threshold --levels 98 100 102 --paths 100 --seed 42 --out threshold.json
python harness.py --strategy controls:cash --out cash.json
```

## Experiment design

This first research slice simulates a single USD equity with USD 10,000 and a long-only whole-share target. Synthetic weekday bars from January 2022 through December 2023 exercise the machinery. They include exchange holidays and convey no evidence of investment returns. Each training window spans six calendar months. The runner selects the highest net marked ending equity from the parameter grid, breaking ties in command-line order, then freezes the winner for six months. Each batch advances twelve months. Jan–Jun 2022 trains the strategy for Jul–Dec 2022. Jan–Jun 2023 trains the next version for Jul–Dec 2023. Each forward replay starts with USD 10,000 and can trade at the first open using its own training history. Only the optional cash control deliberately stays flat. Compare train_return, forward_return, forward_minus_train and the counts of buys and sells across batches. Closing marked equity includes remaining positions. Training scores start flat for each candidate. Training warm-up starts at the fold boundary, while forward decisions have access to preceding closes. The runner marks open shares at the last close and does not simulate liquidation. An order that would exhaust available cash including fees is skipped.

To add a control, create a Python module in the repository and implement a pure function accepting an immutable sequence of prior closes and one numeric parameter. Return a nonnegative integer target share count. Pass its module and function name via `--strategy module:function`. Only load trusted local research code. A decision based on the previous close fills at the next observed open. There is no connection to a broker. Use the controls module as an example.

Each fold records training scores, selected parameter, forward equity, baseline fills with fees, and the endpoint for every neighbouring parameter on the same forward dates. Neighbours are diagnostics; selecting a winner from them consumes that holdout. Each Monte Carlo trial perturbs daily log returns before decisions via seeded Gaussian innovations. A shared daily factor scales open and close and propagates through remaining prices. Each trial recomputes signals, orders, costs and balances from that fold's baseline opening state. Seeds are recorded. These are within-fold market perturbations; calibrated regime changes and execution shocks remain research work.

## Qlib data path

In a compatible environment install Microsoft's `pyqlib` distribution and provide a local US daily Qlib provider. The adapter initializes Qlib and calls `D.features` for the chosen instrument's open and close. It requires actual tradable USD prices and a complete history. Adjusted or normalized prices invalidate dollar-level sizing and commissions. Select a corporate-action-free interval for this prototype. Missing-session and corporate-action reconciliation still require implementation.

```sh
python harness.py --provider /path/to/us_provider --symbol AAPL --start 2022-01-01 --end 2024-01-01 --levels 150 160 170 --out equity.json
```

The end is exclusive. The synthetic runs exercise the replay layer independently of Qlib. The Qlib provider path requires separate integration verification with real provider bytes. [Qlib data documentation](https://qlib.readthedocs.io/en/latest/component/data.html)

## IBKR transaction costs

The selected profile is IBKR Pro US stocks, fixed pricing, standard whole-share orders. This is a research assumption until the account pricing plan is confirmed. The snapshot checked November 22, 2026 applies USD 0.005/share, a USD 1 minimum and a 1% trade-value maximum per filled order. Each rebalance is simulated as one complete order. Regulatory estimates add USD 0.0000206 per dollar sold and USD 0.000003 per share traded; the displayed FINRA trading activity rate on this source snapshot was zero. Preserve unrounded estimates in the ledger. Live statement aggregation, rounding, exemptions and future fee changes can produce differences. The three published base-commission examples are unit-tested. The current snapshot is a constant-cost scenario even when replaying older dates. [IBKR Canada fee schedule](https://www.interactivebrokers.ca/en/pricing/commissions-stocks.php)

## Interpretation and next research work

Reports include parameters, seed, data fingerprint, currency, fold bounds, equity and order records. Compare runs with matching data hashes, calendars, opening capital and fee assumptions. Fold equity includes open positions. USD amounts precede personal taxes, FX conversion, market impact, subscriptions and slippage. Crypto requires its own execution costs and 24/7 calendar before any crypto result is usable.

Next milestones are a pinned Qlib environment with a real provider integration fixture, calendar integrity checks, versioned fee profiles, fitted strategies with leakage-aware internal validation, regime attribution, multi-asset and execution perturbations, and automated matched-run comparison. Later infrastructure includes CAD reporting and tax accounting. Keep all candidate investment strategies downstream of harness validation. See [platform research plan](docs/platform-plan.md) for the full acceptance criteria.

## Fitted strategies and diagnostics

Run the fitted control with `python harness.py --strategy controls:MeanThreshold --levels -1 0 1 --out fitted.json`. A fitted plug-in exposes `fit(rows, parameter)` and `decide(prior_closes, artifact)`. Return an immutable fitted artifact, keep decisions pure and restrict all inputs to the supplied observations. The example learns a mean close and applies a candidate offset.

Within each six-month training batch the first three months fit each candidate and the last three score it chronologically. Select the parameter with the best ending marked equity. Refit on the entire six-month batch before the first forward open and hold the selected artifact fixed during all forward decisions and perturbation trials. Neighbouring parameters are refitted on training data solely for separate sensitivity runs. The earlier static-rule interface retains its six-month grid search. For fitted strategies, selection_return covers the three-month inner validation period. The six-month train_return and forward_minus_train fields are null because their durations would be inconsistent. Compare forward performance across independent batches and inspect the raw equity curves.

Each forward report attributes daily net marked P&L to the direction of the preceding twenty-session return, known before the open. Session counts and dollar changes are additive across regimes, including any sessions without sufficient history. These fields describe the baseline strategy. Fitting and attribution tests use synthetic prices and do not establish profitability.

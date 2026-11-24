# Strategy catalog

Source: Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865. One folder per strategy section. "Harness status" describes the current single-instrument, daily, long/flat harness.

Folders: 174 (153 top-level sections plus 21 sub-variants). Tested: 7. Not testable: 167.

| Not testable reason | Count |
|---|---|
| options chains | 61 |
| bonds/rates | 21 |
| futures | 21 |
| other data not available | 19 |
| cross-sectional universe | 16 |
| not a market trading rule | 15 |
| FX | 6 |
| multiple instruments | 4 |
| needs high/low/volume | 3 |
| intraday ML | 1 |

Tested results are SPY 2016-2026 (2.2 and 2.4: SPY 2024-01 to 2026-11, option bars, see docs/options.md), compounded over the ten July-December forward windows (see each README for caveats).

| Section | Strategy | Asset class | Status | Headline |
|---|---|---|---|---|
| 2.2 | [Covered call](2.2-covered-call/) | Options | tested | 33.7% vs B&H 41.5%, low confidence |
| 2.3 | [Covered put](2.3-covered-put/) | Options | not testable: options chains |  |
| 2.4 | [Protective put](2.4-protective-put/) | Options | tested | 32.5% vs B&H 41.5%, low confidence |
| 2.5 | [Protective call](2.5-protective-call/) | Options | not testable: options chains |  |
| 2.6 | [Bull call spread](2.6-bull-call-spread/) | Options | not testable: options chains |  |
| 2.7 | [Bull put spread](2.7-bull-put-spread/) | Options | not testable: options chains |  |
| 2.8 | [Bear call spread](2.8-bear-call-spread/) | Options | not testable: options chains |  |
| 2.9 | [Bear put spread](2.9-bear-put-spread/) | Options | not testable: options chains |  |
| 2.10 | [Long synthetic forward](2.10-long-synthetic-forward/) | Options | not testable: options chains |  |
| 2.11 | [Short synthetic forward](2.11-short-synthetic-forward/) | Options | not testable: options chains |  |
| 2.12 | [Long combo](2.12-long-combo/) | Options | not testable: options chains |  |
| 2.13 | [Short combo](2.13-short-combo/) | Options | not testable: options chains |  |
| 2.14 | [Bull call ladder](2.14-bull-call-ladder/) | Options | not testable: options chains |  |
| 2.15 | [Bull put ladder](2.15-bull-put-ladder/) | Options | not testable: options chains |  |
| 2.16 | [Bear call ladder](2.16-bear-call-ladder/) | Options | not testable: options chains |  |
| 2.17 | [Bear put ladder](2.17-bear-put-ladder/) | Options | not testable: options chains |  |
| 2.18 | [Calendar call spread](2.18-calendar-call-spread/) | Options | not testable: options chains |  |
| 2.19 | [Calendar put spread](2.19-calendar-put-spread/) | Options | not testable: options chains |  |
| 2.20 | [Diagonal call spread](2.20-diagonal-call-spread/) | Options | not testable: options chains |  |
| 2.21 | [Diagonal put spread](2.21-diagonal-put-spread/) | Options | not testable: options chains |  |
| 2.22 | [Long straddle](2.22-long-straddle/) | Options | not testable: options chains |  |
| 2.23 | [Long strangle](2.23-long-strangle/) | Options | not testable: options chains |  |
| 2.24 | [Long guts](2.24-long-guts/) | Options | not testable: options chains |  |
| 2.25 | [Short straddle](2.25-short-straddle/) | Options | not testable: options chains |  |
| 2.26 | [Short strangle](2.26-short-strangle/) | Options | not testable: options chains |  |
| 2.27 | [Short guts](2.27-short-guts/) | Options | not testable: options chains |  |
| 2.28 | [Long call synthetic straddle](2.28-long-call-synthetic-straddle/) | Options | not testable: options chains |  |
| 2.29 | [Long put synthetic straddle](2.29-long-put-synthetic-straddle/) | Options | not testable: options chains |  |
| 2.30 | [Short call synthetic straddle](2.30-short-call-synthetic-straddle/) | Options | not testable: options chains |  |
| 2.31 | [Short put synthetic straddle](2.31-short-put-synthetic-straddle/) | Options | not testable: options chains |  |
| 2.32 | [Covered short straddle](2.32-covered-short-straddle/) | Options | not testable: options chains |  |
| 2.33 | [Covered short strangle](2.33-covered-short-strangle/) | Options | not testable: options chains |  |
| 2.34 | [Strap](2.34-strap/) | Options | not testable: options chains |  |
| 2.35 | [Strip](2.35-strip/) | Options | not testable: options chains |  |
| 2.36 | [Call ratio backspread](2.36-call-ratio-backspread/) | Options | not testable: options chains |  |
| 2.37 | [Put ratio backspread](2.37-put-ratio-backspread/) | Options | not testable: options chains |  |
| 2.38 | [Ratio call spread](2.38-ratio-call-spread/) | Options | not testable: options chains |  |
| 2.39 | [Ratio put spread](2.39-ratio-put-spread/) | Options | not testable: options chains |  |
| 2.40 | [Long call butterfly](2.40-long-call-butterfly/) | Options | not testable: options chains |  |
| 2.40.1 | [Modified call butterfly](2.40.1-modified-call-butterfly/) | Options | not testable: options chains |  |
| 2.41 | [Long put butterfly](2.41-long-put-butterfly/) | Options | not testable: options chains |  |
| 2.41.1 | [Modified put butterfly](2.41.1-modified-put-butterfly/) | Options | not testable: options chains |  |
| 2.42 | [Short call butterfly](2.42-short-call-butterfly/) | Options | not testable: options chains |  |
| 2.43 | [Short put butterfly](2.43-short-put-butterfly/) | Options | not testable: options chains |  |
| 2.44 | ["Long" iron butterfly](2.44-long-iron-butterfly/) | Options | not testable: options chains |  |
| 2.45 | ["Short" iron butterfly](2.45-short-iron-butterfly/) | Options | not testable: options chains |  |
| 2.46 | [Long call condor](2.46-long-call-condor/) | Options | not testable: options chains |  |
| 2.47 | [Long put condor](2.47-long-put-condor/) | Options | not testable: options chains |  |
| 2.48 | [Short call condor](2.48-short-call-condor/) | Options | not testable: options chains |  |
| 2.49 | [Short put condor](2.49-short-put-condor/) | Options | not testable: options chains |  |
| 2.50 | [Long iron condor](2.50-long-iron-condor/) | Options | not testable: options chains |  |
| 2.51 | [Short iron condor](2.51-short-iron-condor/) | Options | not testable: options chains |  |
| 2.52 | [Long box](2.52-long-box/) | Options | not testable: options chains |  |
| 2.53 | [Collar](2.53-collar/) | Options | not testable: options chains |  |
| 2.54 | [Bullish short seagull spread](2.54-bullish-short-seagull-spread/) | Options | not testable: options chains |  |
| 2.55 | [Bearish long seagull spread](2.55-bearish-long-seagull-spread/) | Options | not testable: options chains |  |
| 2.56 | [Bearish short seagull spread](2.56-bearish-short-seagull-spread/) | Options | not testable: options chains |  |
| 2.57 | [Bullish long seagull spread](2.57-bullish-long-seagull-spread/) | Options | not testable: options chains |  |
| 3.1 | [Price-momentum](3.1-price-momentum/) | Stocks | not testable: cross-sectional universe |  |
| 3.2 | [Earnings-momentum](3.2-earnings-momentum/) | Stocks | not testable: cross-sectional universe |  |
| 3.3 | [Value](3.3-value/) | Stocks | not testable: cross-sectional universe |  |
| 3.4 | [Low-volatility anomaly](3.4-low-volatility-anomaly/) | Stocks | not testable: cross-sectional universe |  |
| 3.5 | [Implied volatility](3.5-implied-volatility/) | Stocks | not testable: options chains |  |
| 3.6 | [Multifactor portfolio](3.6-multifactor-portfolio/) | Stocks | not testable: cross-sectional universe |  |
| 3.7 | [Residual momentum](3.7-residual-momentum/) | Stocks | not testable: cross-sectional universe |  |
| 3.8 | [Pairs trading](3.8-pairs-trading/) | Stocks | not testable: multiple instruments |  |
| 3.9 | [Mean-reversion - single cluster](3.9-mean-reversion-single-cluster/) | Stocks | not testable: cross-sectional universe |  |
| 3.9.1 | [Mean-reversion - multiple clusters](3.9.1-mean-reversion-multiple-clusters/) | Stocks | not testable: cross-sectional universe |  |
| 3.10 | [Mean-reversion - weighted regression](3.10-mean-reversion-weighted-regression/) | Stocks | not testable: cross-sectional universe |  |
| 3.11 | [Single moving average](3.11-single-moving-average/) | Stocks | tested | 21.7% vs B&H 46.8%, cash 0% |
| 3.12 | [Two moving averages](3.12-two-moving-averages/) | Stocks | tested | 23.4% vs B&H 46.8%, cash 0%; long/short variant 2.8% |
| 3.13 | [Three moving averages](3.13-three-moving-averages/) | Stocks | tested | 15.5% vs B&H 46.8%, cash 0% |
| 3.14 | [Support and resistance](3.14-support-and-resistance/) | Stocks | not testable: needs high/low/volume |  |
| 3.15 | [Channel](3.15-channel/) | Stocks | tested | 15.9% vs B&H 46.8%, cash 0% |
| 3.16 | [Event-driven - M&A](3.16-event-driven-manda/) | Stocks | not testable: other data not available |  |
| 3.17 | [Machine learning - single-stock KNN](3.17-machine-learning-single-stock-knn/) | Stocks | not testable: needs high/low/volume |  |
| 3.18 | [Statistical arbitrage - optimization](3.18-statistical-arbitrage-optimization/) | Stocks | not testable: cross-sectional universe |  |
| 3.19 | [Market-making](3.19-market-making/) | Stocks | not testable: other data not available |  |
| 3.20 | [Alpha combos](3.20-alpha-combos/) | Stocks | not testable: cross-sectional universe |  |
| 4.1 | [Sector momentum rotation](4.1-sector-momentum-rotation/) | Exchange-traded funds | not testable: cross-sectional universe |  |
| 4.1.1 | [Sector momentum rotation with MA filter](4.1.1-sector-momentum-rotation-with-ma-filter/) | Exchange-traded funds | not testable: cross-sectional universe |  |
| 4.1.2 | [Dual-momentum sector rotation](4.1.2-dual-momentum-sector-rotation/) | Exchange-traded funds | not testable: cross-sectional universe |  |
| 4.2 | [Alpha rotation](4.2-alpha-rotation/) | Exchange-traded funds | not testable: cross-sectional universe |  |
| 4.3 | [R-squared](4.3-r-squared/) | Exchange-traded funds | not testable: cross-sectional universe |  |
| 4.4 | [Mean-reversion](4.4-mean-reversion/) | Exchange-traded funds | not testable: needs high/low/volume |  |
| 4.5 | [Leveraged ETFs (LETFs)](4.5-leveraged-etfs-letfs/) | Exchange-traded funds | not testable: multiple instruments |  |
| 4.6 | [Multi-asset trend following](4.6-multi-asset-trend-following/) | Exchange-traded funds | not testable: multiple instruments |  |
| 5.2 | [Bullets](5.2-bullets/) | Fixed income | not testable: bonds/rates |  |
| 5.3 | [Barbells](5.3-barbells/) | Fixed income | not testable: bonds/rates |  |
| 5.4 | [Ladders](5.4-ladders/) | Fixed income | not testable: bonds/rates |  |
| 5.5 | [Bond immunization](5.5-bond-immunization/) | Fixed income | not testable: bonds/rates |  |
| 5.6 | [Dollar-duration-neutral butterfly](5.6-dollar-duration-neutral-butterfly/) | Fixed income | not testable: bonds/rates |  |
| 5.7 | [Fifty-fifty butterfly](5.7-fifty-fifty-butterfly/) | Fixed income | not testable: bonds/rates |  |
| 5.8 | [Regression-weighted butterfly](5.8-regression-weighted-butterfly/) | Fixed income | not testable: bonds/rates |  |
| 5.8.1 | [Maturity-weighted butterfly](5.8.1-maturity-weighted-butterfly/) | Fixed income | not testable: bonds/rates |  |
| 5.9 | [Low-risk factor](5.9-low-risk-factor/) | Fixed income | not testable: bonds/rates |  |
| 5.10 | [Value factor](5.10-value-factor/) | Fixed income | not testable: bonds/rates |  |
| 5.11 | [Carry factor](5.11-carry-factor/) | Fixed income | not testable: bonds/rates |  |
| 5.12 | [Rolling down the yield curve](5.12-rolling-down-the-yield-curve/) | Fixed income | not testable: bonds/rates |  |
| 5.13 | [Yield curve spread (flatteners & steepeners)](5.13-yield-curve-spread-flatteners-and-steepeners/) | Fixed income | not testable: bonds/rates |  |
| 5.14 | [CDS basis arbitrage](5.14-cds-basis-arbitrage/) | Fixed income | not testable: bonds/rates |  |
| 5.15 | [Swap-spread arbitrage](5.15-swap-spread-arbitrage/) | Fixed income | not testable: bonds/rates |  |
| 6.2 | [Cash-and-carry arbitrage](6.2-cash-and-carry-arbitrage/) | Indexes | not testable: futures |  |
| 6.3 | [Dispersion trading in equity indexes](6.3-dispersion-trading-in-equity-indexes/) | Indexes | not testable: options chains |  |
| 6.3.1 | [Dispersion trading - subset portfolio](6.3.1-dispersion-trading-subset-portfolio/) | Indexes | not testable: options chains |  |
| 6.4 | [Intraday arbitrage between index ETFs](6.4-intraday-arbitrage-between-index-etfs/) | Indexes | not testable: multiple instruments |  |
| 6.5 | [Index volatility targeting with risk-free asset](6.5-index-volatility-targeting-with-risk-free-asset/) | Indexes | tested | 34.6% vs B&H 46.8%, cash 0% |
| 7.2 | [VIX futures basis trading](7.2-vix-futures-basis-trading/) | Volatility | not testable: futures |  |
| 7.3 | [Volatility carry with two ETNs](7.3-volatility-carry-with-two-etns/) | Volatility | not testable: futures |  |
| 7.3.1 | [Hedging short VXX with VIX futures](7.3.1-hedging-short-vxx-with-vix-futures/) | Volatility | not testable: futures |  |
| 7.4 | [Volatility risk premium](7.4-volatility-risk-premium/) | Volatility | not testable: futures |  |
| 7.4.1 | [Volatility risk premium with Gamma hedging](7.4.1-volatility-risk-premium-with-gamma-hedging/) | Volatility | not testable: futures |  |
| 7.5 | [Volatility skew - long risk reversal](7.5-volatility-skew-long-risk-reversal/) | Volatility | not testable: futures |  |
| 7.6 | [Volatility trading with variance swaps](7.6-volatility-trading-with-variance-swaps/) | Volatility | not testable: futures |  |
| 8.1 | [Moving averages with HP filter](8.1-moving-averages-with-hp-filter/) | Foreign exchange | not testable: FX |  |
| 8.2 | [Carry trade](8.2-carry-trade/) | Foreign exchange | not testable: FX |  |
| 8.2.1 | [High-minus-low carry](8.2.1-high-minus-low-carry/) | Foreign exchange | not testable: FX |  |
| 8.3 | [Dollar carry trade](8.3-dollar-carry-trade/) | Foreign exchange | not testable: FX |  |
| 8.4 | [Momentum & carry combo](8.4-momentum-and-carry-combo/) | Foreign exchange | not testable: FX |  |
| 8.5 | [FX triangular arbitrage](8.5-fx-triangular-arbitrage/) | Foreign exchange | not testable: FX |  |
| 9.1 | [Roll yields](9.1-roll-yields/) | Commodities | not testable: futures |  |
| 9.2 | [Trading based on hedging pressure](9.2-trading-based-on-hedging-pressure/) | Commodities | not testable: futures |  |
| 9.3 | [Portfolio diversification with commodities](9.3-portfolio-diversification-with-commodities/) | Commodities | not testable: futures |  |
| 9.4 | [Value](9.4-value/) | Commodities | not testable: futures |  |
| 9.5 | [Skewness premium](9.5-skewness-premium/) | Commodities | not testable: futures |  |
| 9.6 | [Trading with pricing models](9.6-trading-with-pricing-models/) | Commodities | not testable: futures |  |
| 10.1 | [Hedging risk with futures](10.1-hedging-risk-with-futures/) | Futures | not testable: futures |  |
| 10.1.1 | [Cross-hedging](10.1.1-cross-hedging/) | Futures | not testable: futures |  |
| 10.1.2 | [Interest rate risk hedging](10.1.2-interest-rate-risk-hedging/) | Futures | not testable: futures |  |
| 10.2 | [Calendar spread](10.2-calendar-spread/) | Futures | not testable: futures |  |
| 10.3 | [Contrarian trading (mean-reversion)](10.3-contrarian-trading-mean-reversion/) | Futures | not testable: futures |  |
| 10.3.1 | [Contrarian trading - market activity](10.3.1-contrarian-trading-market-activity/) | Futures | not testable: futures |  |
| 10.4 | [Trend following (momentum)](10.4-trend-following-momentum/) | Futures | not testable: futures |  |
| 11.2 | [Carry, equity tranche - index hedging](11.2-carry-equity-tranche-index-hedging/) | Structured assets | not testable: bonds/rates |  |
| 11.3 | [Carry, senior/mezzanine - index hedging](11.3-carry-senior-mezzanine-index-hedging/) | Structured assets | not testable: bonds/rates |  |
| 11.4 | [Carry - tranche hedging](11.4-carry-tranche-hedging/) | Structured assets | not testable: bonds/rates |  |
| 11.5 | [Carry - CDS hedging](11.5-carry-cds-hedging/) | Structured assets | not testable: bonds/rates |  |
| 11.6 | [CDOs - curve trades](11.6-cdos-curve-trades/) | Structured assets | not testable: bonds/rates |  |
| 11.7 | [Mortgage-backed security (MBS) trading](11.7-mortgage-backed-security-mbs-trading/) | Structured assets | not testable: bonds/rates |  |
| 12.1 | [Convertible arbitrage](12.1-convertible-arbitrage/) | Convertibles | not testable: options chains |  |
| 12.2 | [Convertible option-adjusted spread](12.2-convertible-option-adjusted-spread/) | Convertibles | not testable: options chains |  |
| 13.1 | [Municipal bond tax arbitrage](13.1-municipal-bond-tax-arbitrage/) | Tax arbitrage | not testable: not a market trading rule |  |
| 13.2 | [Cross-border tax arbitrage](13.2-cross-border-tax-arbitrage/) | Tax arbitrage | not testable: not a market trading rule |  |
| 13.2.1 | [Cross-border tax arbitrage with options](13.2.1-cross-border-tax-arbitrage-with-options/) | Tax arbitrage | not testable: not a market trading rule |  |
| 14.1 | [Inflation hedging - inflation swaps](14.1-inflation-hedging-inflation-swaps/) | Miscellaneous assets | not testable: other data not available |  |
| 14.2 | [TIPS-Treasury arbitrage](14.2-tips-treasury-arbitrage/) | Miscellaneous assets | not testable: other data not available |  |
| 14.3 | [Weather risk - demand hedging](14.3-weather-risk-demand-hedging/) | Miscellaneous assets | not testable: other data not available |  |
| 14.4 | [Energy - spark spread](14.4-energy-spark-spread/) | Miscellaneous assets | not testable: other data not available |  |
| 15.1 | [Buying and holding distressed debt](15.1-buying-and-holding-distressed-debt/) | Distressed assets | not testable: not a market trading rule |  |
| 15.2 | [Active distressed investing](15.2-active-distressed-investing/) | Distressed assets | not testable: not a market trading rule |  |
| 15.2.1 | [Planning a reorganization](15.2.1-planning-a-reorganization/) | Distressed assets | not testable: not a market trading rule |  |
| 15.2.2 | [Buying outstanding debt](15.2.2-buying-outstanding-debt/) | Distressed assets | not testable: not a market trading rule |  |
| 15.2.3 | [Loan-to-own](15.2.3-loan-to-own/) | Distressed assets | not testable: not a market trading rule |  |
| 15.3 | [Distress risk puzzle](15.3-distress-risk-puzzle/) | Distressed assets | not testable: not a market trading rule |  |
| 15.3.1 | [Distress risk puzzle - risk management](15.3.1-distress-risk-puzzle-risk-management/) | Distressed assets | not testable: not a market trading rule |  |
| 16.2 | [Mixed-asset diversification with real estate](16.2-mixed-asset-diversification-with-real-estate/) | Real estate | not testable: other data not available |  |
| 16.3 | [Intra-asset diversification within real estate](16.3-intra-asset-diversification-within-real-estate/) | Real estate | not testable: other data not available |  |
| 16.3.1 | [Property type diversification](16.3.1-property-type-diversification/) | Real estate | not testable: other data not available |  |
| 16.3.2 | [Economic diversification](16.3.2-economic-diversification/) | Real estate | not testable: other data not available |  |
| 16.3.3 | [Property type and geographic diversification](16.3.3-property-type-and-geographic-diversification/) | Real estate | not testable: other data not available |  |
| 16.4 | [Real estate momentum - regional approach](16.4-real-estate-momentum-regional-approach/) | Real estate | not testable: other data not available |  |
| 16.5 | [Inflation hedging with real estate](16.5-inflation-hedging-with-real-estate/) | Real estate | not testable: other data not available |  |
| 16.6 | [Fix-and-flip](16.6-fix-and-flip/) | Real estate | not testable: other data not available |  |
| 17.2 | [Money laundering - the dark side of cash](17.2-money-laundering-the-dark-side-of-cash/) | Cash | not testable: not a market trading rule |  |
| 17.3 | [Liquidity management](17.3-liquidity-management/) | Cash | not testable: not a market trading rule |  |
| 17.4 | [Repurchase agreement (REPO)](17.4-repurchase-agreement-repo/) | Cash | not testable: not a market trading rule |  |
| 17.5 | [Pawnbroking](17.5-pawnbroking/) | Cash | not testable: not a market trading rule |  |
| 17.6 | [Loan sharking](17.6-loan-sharking/) | Cash | not testable: not a market trading rule |  |
| 18.2 | [Artificial neural network (ANN)](18.2-artificial-neural-network-ann/) | Cryptocurrencies | not testable: intraday ML |  |
| 18.3 | [Sentiment analysis - naive Bayes Bernoulli](18.3-sentiment-analysis-naive-bayes-bernoulli/) | Cryptocurrencies | not testable: other data not available |  |
| 19.2 | [Fundamental macro momentum](19.2-fundamental-macro-momentum/) | Global macro | not testable: other data not available |  |
| 19.3 | [Global macro inflation hedge](19.3-global-macro-inflation-hedge/) | Global macro | not testable: other data not available |  |
| 19.4 | [Global fixed-income strategy](19.4-global-fixed-income-strategy/) | Global macro | not testable: other data not available |  |
| 19.5 | [Trading on economic announcements](19.5-trading-on-economic-announcements/) | Global macro | not testable: other data not available |  |

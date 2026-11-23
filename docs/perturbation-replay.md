# Perturbation replay

Use this daily-bar fixture to verify the replay mechanics.

```sh
python harness.py --strategy controls:MeanThreshold --levels -1 0 1 --paths 100 --seed 7 --shock-bps 10 --max-delay-sessions 2 --max-half-spread-bps 15 --reject-probability 0.05 --neighbour-steps 1 --out stress.json
```

Each forward path begins with the fold's starting balance and pre-forward close history. A seeded Gaussian innovation in log returns changes subsequent prices. The strategy sees each perturbed close only after that session's execution. The remaining inputs use independent deterministic random streams so the same seed can isolate the effect of each assumption.

| Input | Path behavior |
|---|---|
| Maximum delay in observed sessions | Draw one integer delay uniformly per path. Queue the decision's target until the specified bar. On arrival, resize it against the actual current holdings. Targets outstanding at expiry do not execute. |
| Maximum half spread in basis points | Draw one half spread uniformly per path. Increase the simulated open for purchases and reduce it for sales. Calculate cash and IBKR fees from that fill price. Closing portfolio marks use the market close. |
| Rejection probability | Draw once per session. Skip the scheduled rebalance on a rejection, retain current holdings, and allow later targets to trade. |
| Neighbour steps | Choose once per path from existing sorted candidate levels up to this many grid steps from the selected level. The chosen candidate already has an artifact fitted on the training window. |

The default run enables only the existing price innovation. Set all four stress switches and `--shock-bps` to zero to reproduce baseline trading. To attribute changes, run one family at a time and then a joint run with identical dates, grid, seed and path count. User-chosen bounds express hypothetical stress scenarios; calibrate them with data available before the forward period when interpreting probabilities.

Reports record each path's settings, seed, ending equity difference, maximum marked drawdown as a positive fraction, and fill changes against the baseline. A fill matches on execution date and signed share quantity. A change in price alone can change P&L without changing the count of matched fills. Daily bars support whole-session execution delays; within-session latency, order queue position, and partial fills need richer data and execution models.

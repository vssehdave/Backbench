"""ORB with 5, 10 and 15-minute ranges on the monthly point-in-time top-50 S&P 500 stocks, plus the per-stock study.

Run from the repo root: python strategies/intraday/orb-top50/run.py. Needs Alpaca keys in .env and the EDGAR cache
(python fetch_edgar.py). Writes results.json, results/REPORT.md and one folder per run next to this file. See README.md.
"""
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import intraday as I
import orb_analysis as A
import orb_universe as U
import xs_data

START, END = date(2020, 1, 1), date(2026, 11, 21)  # END exclusive; Fri 2026-11-20 is the last full session
DAILY_START = date(2016, 1, 1)
FIRST_HALF_END = date(2022, 12, 31)
MINUTES, SLIPS, BASE_SLIP = (5, 10, 15), (0, 2, 5), 2
TOP_N, RISK, LEVERAGE, EQUITY, STAT_NOTIONAL = 50, 0.01, 4., 100000., 10000.
FEATURES = ("range_pct", "atr_pct", "gap_abs", "dollar_volume", "beta", "price", "cap_rank")
HERE = Path(__file__).parent


def collect(universe, cal, minutes):
    """{(minutes, short, slip): [(iso day, symbol, trade, range width)]} over every month of the universe."""
    out = {}
    with ProcessPoolExecutor() as pool:
        jobs = [pool.submit(I.month_trades, y, m, picks, minutes, SLIPS, END, cal) for (y, m), picks in sorted(universe.items())]
        for job in jobs:
            for key, rows in job.result().items():
                out.setdefault(key, []).extend(rows)
    return out


def simulate(rows, sessions, max_positions):
    """Equity curve and sized trades for one config. Each day is sized from the equity at its start."""
    by_day = {}
    for iso, symbol, t, _ in rows:
        by_day.setdefault(date.fromisoformat(iso), []).append((symbol, t))
    equity, curve, log = EQUITY, [], []
    for day in sessions:
        for symbol, pnl, fee, notional, t in I.settle(I.size_trades(by_day.get(day, []), equity, RISK, LEVERAGE, max_positions)):
            equity += pnl
            log.append((day, symbol, t, notional, fee, pnl))
        curve.append((day, equity))
    return curve, log


def summarise(curve, log, slip):
    trades = [(d, pnl, pnl / notional) for d, _, _, notional, _, pnl in log]
    cost = sum(fee + notional * slip / 10000 * 2 for _, _, _, notional, fee, _ in log)
    out = I.metrics(curve, trades, cost)
    start_equity = dict(zip((d for d, _ in curve), [EQUITY] + [v for _, v in curve]))
    out["max_notional_pct_of_equity"] = max((n / start_equity[d] for d, _, _, n, _, _ in log), default=0) * 100
    return out


def run_grid(rows_by_config, sessions, max_positions):
    result = {}
    for (m, short, slip), rows in sorted(rows_by_config.items()):
        curve, log = simulate(rows, sessions, max_positions)
        result[(m, short, slip)] = (curve, log, summarise(curve, log, slip))
    return result


def analysis_trades(rows, top, daily, hl, sectors, spy):
    """Fixed-notional trades with features known before entry (see orb_universe). The range is complete before entry."""
    histories, rank = {}, {}
    for month, picks in top.items():
        rank[month] = {s: i + 1 for i, (s, _) in enumerate(picks)}
    out = []
    for iso, symbol, t, width in rows:
        day = date.fromisoformat(iso)
        h = histories.get(symbol) or histories.setdefault(symbol, U.History(daily[symbol], hl[symbol], spy))
        shares = max(math.floor(STAT_NOTIONAL / t["entry"]), 1)
        _, pnl, _, notional, _ = I.settle([(symbol, t, shares)])[0]
        gap = h.gap(day)
        out.append(dict(day=day, symbol=symbol, side=t["side"], pnl=pnl, ret=pnl / notional, f=dict(
            range_pct=width, atr_pct=h.atr_pct(day), gap_abs=abs(gap) if gap is not None else None,
            dollar_volume=h.dollar_volume(day), beta=h.beta(day), price=h.prior_close(day),
            cap_rank=rank[(day.year, day.month)][symbol], sector=sectors.get(symbol, "unknown"))))
    return out


def study(trades):
    first, second = A.split(trades, FIRST_HALF_END)
    out = dict(
        per_stock=A.stock_stats(trades),
        features={f: A.quintiles(trades, f) for f in FEATURES},
        features_first_half={f: A.quintiles(first, f) for f in FEATURES},
        features_second_half={f: A.quintiles(second, f) for f in FEATURES},
        sectors=A.by_category(trades, "sector"),
        persistence=A.persistence(first, second),
        rules=A.feature_rules(first, second, FEATURES),
        winners_vs_rest=A.winners_vs_rest(trades, FEATURES),
        winners_vs_rest_first_half=A.winners_vs_rest(first, FEATURES, min_trades=60),
        chance=A.shuffle_test(trades, FIRST_HALF_END, sims=200))
    c = out["chance"]
    # Binomial cross-check of the shuffle: independent stocks, one-sided P(t > 2) = 0.0228 under no edge.
    p, n, k = 0.0228, c["stocks_tested"], c["observed_count_t_over_2"]
    c["binomial_expected_t_over_2"] = n * p
    c["binomial_p_at_least_observed"] = sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
    out["pooled"] = dict(trades=len(trades), mean_bps=A.mean_t([t["ret"] for t in trades])[0] * 1e4,
                         first_half_bps=A.mean_t([t["ret"] for t in first])[0] * 1e4,
                         second_half_bps=A.mean_t([t["ret"] for t in second])[0] * 1e4,
                         first_half_trades=len(first), second_half_trades=len(second))
    return out


def label(key):
    m, short, slip = key
    return f"{m}min {'long-short' if short else 'long-only'} {slip}bps"


def write_run_folder(folder, name, description, runs, curve, log, spy_curve):
    """One strategy folder: README.md and the standard report of the 2 bps run (results/, mc_results.json)."""
    table = ["| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |",
             "|---|---|---|---|---|---|---|---|"]
    for slip, r in runs.items():
        table.append(f"| {slip} bps | {fmt_pct(r['cagr'])} | {r['sharpe']:.2f} | {fmt_pct(r['max_drawdown'])} | {r['trades']} | "
                     f"{fmt_pct(r['win_rate'])} | {r['avg_trade_bps']:.1f} | {r['max_notional_pct_of_equity']:.1f} |")
    I.write_standard_report(folder / "results", folder / "mc_results.json", name, curve, spy_curve, I.orb_fills(log))
    (folder / "README.md").write_text("\n".join([
        f"# {name}", "", description, "",
        "Generated by ../run.py (python strategies/intraday/orb-top50/run.py from the repo root); see ../README.md for the "
        "rules, data, the per-stock analysis and caveats.", "", *table, "", "results/ holds the standard report of the 2 bps run: "
        "REPORT.md (metrics, Monte Carlo drawdown, equity.svg), report.json and the best, worst and random day trade logs."]) + "\n", encoding="utf-8")


def fmt_pct(x):
    return f"{x * 100:.1f}%"


def write_report(report, results_dir):
    L = ["# intraday-orb-top50", "", "## Range x side x slippage (monthly point-in-time top 50, notional capped at equity / 50)", "",
         "| config | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |", "|---|---|---|---|---|---|---|---|"]
    for name, r in report["runs"].items():
        L.append(f"| {name} | {fmt_pct(r['cagr'])} | {r['sharpe']:.2f} | {fmt_pct(r['max_drawdown'])} | {r['trades']} | "
                 f"{fmt_pct(r['win_rate'])} | {r['avg_trade_bps']:.1f} | {r['max_notional_pct_of_equity']:.1f} |")
    for name, r in report["benchmarks"].items():
        m = r["metrics"]
        L.append(f"| {name} buy and hold | {fmt_pct(m['cagr'])} | {m['sharpe']:.2f} | {fmt_pct(m['max_drawdown'])} | | | | |")
    L += ["", "## Sensitivity: notional capped at equity / 10 instead of / 50 (2 bps)", "",
          "| config | CAGR | Sharpe | max DD | trades | avg trade bps |", "|---|---|---|---|---|---|"]
    for name, r in report["cap_equity_over_10"].items():
        L.append(f"| {name} | {fmt_pct(r['cagr'])} | {r['sharpe']:.2f} | {fmt_pct(r['max_drawdown'])} | {r['trades']} | {r['avg_trade_bps']:.1f} |")
    L += ["", "## Old 5-minute config (monthly top 20 by dollar volume from the 103 candidates), sizing cap off vs on", "",
          "| config | cap | CAGR | Sharpe | max DD | trades | max position % equity |", "|---|---|---|---|---|---|---|"]
    for name, r in report["old_config"].items():
        L.append(f"| {name} | {r['cap']} | {fmt_pct(r['cagr'])} | {r['sharpe']:.2f} | {fmt_pct(r['max_drawdown'])} | {r['trades']} | "
                 f"{r['max_notional_pct_of_equity']:.0f} |")
    for m, s in report["study"].items():
        L += ["", f"## {m}-minute range, long-short, 2 bps: per stock (fixed ${STAT_NOTIONAL:,.0f} per trade, 100+ trades, "
              "top and bottom 10 by total P&L)", ""]
        stats = s["per_stock"]
        rank = sorted((k for k in stats if stats[k]["n"] >= 100), key=lambda k: -stats[k]["pnl"])
        L += ["| symbol | trades | total P&L USD | mean bps/trade | win rate | profit factor |", "|---|---|---|---|---|---|"]
        for k in rank[:10] + ["..."] + rank[-10:]:
            if k == "...":
                L.append("| ... | | | | | |")
                continue
            v = stats[k]
            L.append(f"| {k} | {v['n']} | {v['pnl']:,.0f} | {v['mean_bps']:.1f} | {fmt_pct(v['win_rate'])} | {v['profit_factor']:.2f} |")
        for key, title in (("winners_vs_rest", "2020-2026"), ("winners_vs_rest_first_half", "2020-2022 only")):
            w = s[key]
            L += ["", f"Winners (top 20% of {w['eligible']} stocks by total P&L, {title}) vs the rest: median of per-stock mean "
                  "feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: " + ", ".join(w["winners"]), "",
                  "| feature | winners median | rest median | rho with stock P&L |", "|---|---|---|---|"]
            for f, v in w["features"].items():
                L.append(f"| {f} | {v['winners_median']:.4g} | {v['rest_median']:.4g} | {v['rho_with_pnl']:.2f} |")
            L += ["", "Sectors (winners / rest): " + "; ".join(f"{k} {a}/{b}" for k, (a, b) in sorted(w["sectors"].items()))]
        L += ["", "Features vs per-trade return, all trades pooled (Spearman rho; mean bps of lowest and highest quintile; "
              "first half 2020-2022 and second half 2023-2026 bottom/top bps).", "",
              "| feature | n | rho | bottom bps | top bps | top-bottom | first half rho | second half rho |", "|---|---|---|---|---|---|---|---|"]
        for f, v in s["features"].items():
            L.append(f"| {f} | {v['n']} | {v['rho']:.3f} | {v['bottom_bps']:.1f} | {v['top_bps']:.1f} | {v['top_minus_bottom_bps']:.1f} | "
                     f"{s['features_first_half'][f]['rho']:.3f} | {s['features_second_half'][f]['rho']:.3f} |")
        L += ["", "Sector (today's S&P membership; stocks since removed are 'unknown'): " + "; ".join(
            f"{k} {n} trades {b:.1f} bps" for k, (n, b) in s["sectors"].items())]
        p, c = s["persistence"], s["chance"]
        L += ["", f"Stock picks: top 20% by mean bps in 2020-2022 ({len(p['picked'])} of {p['eligible']} stocks with 60+ trades): "
              f"{p['picked_first_half_bps']:.1f} bps in sample, {p['picked_second_half_bps']:.1f} bps in 2023-2026 "
              f"({p['picked_second_half_trades']} trades, P&L {p['picked_second_half_pnl']:,.0f} USD) versus "
              f"{p['rest_second_half_bps']:.1f} for the other stocks and {p['all_second_half_bps']:.1f} for all. "
              f"Rank correlation of per-stock mean, first vs second half: {p['rank_corr_first_vs_second']:.2f} "
              f"over {p['stocks_in_rank_corr']} stocks.", "",
              f"Chance ({c['sims']} within-day shuffles of returns across stocks): stocks with t > 2 observed {c['observed_count_t_over_2']} "
              f"vs {c['chance_count_mean']:.1f} expected (95th pct {c['chance_count_p95']}) of {c['stocks_tested']} stocks with 50+ trades "
              f"(binomial with independent stocks: {c['binomial_expected_t_over_2']:.1f} expected, P(at least observed) = "
              f"{c['binomial_p_at_least_observed']:.2f}); largest t "
              f"{c['observed_max_t']:.2f} vs {c['chance_max_t_mean']:.2f} (95th pct {c['chance_max_t_p95']:.2f}); second-half bps of "
              f"first-half picks {c['observed_second_half_bps_of_first_half_picks']:.1f} vs {c['chance_second_half_bps_mean']:.1f} "
              f"(95th pct {c['chance_second_half_bps_p95']:.1f}, p = {c['p_value_second_half']:.2f}).", "",
              "Feature rules, tercile cut points from 2020-2022 only:", "",
              "| feature | rule | 2020-2022 bps (n) | 2023-2026 bps (n) | 2023-2026 naive t |", "|---|---|---|---|---|"]
        for r in s["rules"]:
            L.append(f"| {r['feature']} | {r['rule']} tercile | {r['first_half_bps']:.1f} ({r['first_half_n']}) | "
                     f"{r['second_half_bps']:.1f} ({r['second_half_n']}) | {r['second_half_t']:.1f} |")
    L += ["", "Each run has its own folder next to this one (5min-long-short, ..., old-5min-top20-capped) with its README, "
          "results/REPORT.md (metrics, Monte Carlo drawdown, equity.svg), report.json and 2 bps trade logs. Full numbers are "
          "in ../results.json."]
    (results_dir / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    started = time.time()
    clock = {}

    def lap(name):
        clock[name] = round(time.time() - started)
        print(name, clock[name], flush=True)

    panel = xs_data.build_panel(date(2015, 1, 1), date(2026, 11, 1))
    shares = U.load_shares(sorted(panel.adj))
    cal = I.calendar(DAILY_START, END)
    sessions = sorted(d for d in cal if d >= START)
    months = sorted({(d.year, d.month) for d in sessions})
    top = U.top_by_cap(panel, shares, months, TOP_N)
    universe = {k: [s for s, _ in v] for k, v in top.items()}
    pairs = sorted({(s, y, m) for (y, m), picked in universe.items() for s in picked})
    I.prefetch(pairs, END, cal, workers=6)
    symbols = sorted({s for s, _, _ in pairs} | {"SPY"})
    daily = I.merge_daily(I.daily_bars(symbols, DAILY_START, END, "raw"), I.daily_bars(symbols, DAILY_START, END, "all"))
    hl = U.daily_hl(symbols, DAILY_START, END)
    lap("data")
    rows = collect(universe, cal, MINUTES)
    lap("signals")
    grid = run_grid(rows, sessions, TOP_N)
    lap("simulate")
    # Sensitivity: the 1 USD IBKR minimum commission is about 10 bps round trip on a 2% position, so also try 10% positions.
    wide = {k: v[2] for k, v in run_grid({k: r for k, r in rows.items() if k[2] == BASE_SLIP}, sessions, 10).items()}

    hold = {"SPY": I.buy_hold(daily, lambda d: ["SPY"], sessions)}
    sectors = U.sectors()
    study_out = {}
    for m in MINUTES:
        trades = analysis_trades(rows[(m, True, BASE_SLIP)], top, daily, hl, sectors, daily["SPY"])
        study_out[m] = study(trades)
        lap(f"study {m}")

    # Old config: monthly top 20 by dollar volume from the fixed candidates, 5-minute range, with and without the cap.
    old_symbols = list(I.CANDIDATES) + ["SPY"]
    old_daily = I.merge_daily(I.daily_bars(old_symbols, DAILY_START, END, "raw"), I.daily_bars(old_symbols, DAILY_START, END, "all"))
    old_universe = I.monthly_universe({s: old_daily[s] for s in I.CANDIDATES if s in old_daily}, months)
    I.prefetch(sorted({(s, y, m) for (y, m), p in old_universe.items() for s in p}), END, cal, workers=6)
    old_rows = collect(old_universe, cal, (5,))
    old, old_capped = {}, None
    for cap_name, cap in (("none", None), ("equity/20", 20)):
        old_grid = run_grid(old_rows, sessions, cap)
        old_capped = old_grid if cap else old_capped
        for key, (_, _, r) in old_grid.items():
            if key[2] in (0, 2, 5):
                old[f"{label(key)} cap {cap_name}"] = dict(r, cap=cap_name)
    lap("old config")

    report = dict(
        period=dict(start=str(sessions[0]), end_exclusive=str(END), last_session=str(sessions[-1]), sessions=len(sessions)),
        rules=dict(risk_per_trade=RISK, leverage_cap=LEVERAGE, notional_cap="equity / 50", start_equity=EQUITY,
                   slippage_bps=SLIPS, ranges=MINUTES, first_half_end=str(FIRST_HALF_END)),
        universe=dict(top_n=TOP_N, months=len(months), distinct=len({s for s, _, _ in pairs}), symbol_months=len(pairs),
                      members_without_edgar_facts=len(set(panel.adj) - set(shares)),
                      meta_and_berkshire_in_universe=sorted({"META", "BRK.B", "FB", "BRK.A"} & {s for s, _, _ in pairs})),
        benchmarks={k: dict(metrics=I.metrics(v), yearly=I.yearly(v)) for k, v in hold.items()},
        runs={label(k): dict(v[2], yearly=I.yearly(v[0]) if k[2] == BASE_SLIP else None) for k, v in grid.items()},
        cap_equity_over_10={label(k): v for k, v in wide.items()}, old_config=old, study=study_out, seconds=clock)
    (HERE / "results.json").write_text(json.dumps(report, indent=1, default=str), encoding="utf-8")
    (HERE / "results").mkdir(exist_ok=True)
    write_report(report, HERE / "results")
    for m in MINUTES:
        for short in (True, False):
            side = "long-short" if short else "long-only"
            curve, log, _ = grid[(m, short, BASE_SLIP)]
            write_run_folder(HERE / f"{m}min-{side}", f"intraday-orb-top50-{m}min-{side}",
                             f"{m}-minute opening range breakout, {side}, on the monthly point-in-time top {TOP_N} S&P 500 stocks "
                             f"by market cap, {sessions[0]} to {sessions[-1]}. Fixed 1% risk per trade, each position capped at "
                             f"equity / {TOP_N} so gross never exceeds equity. IBKR fees plus per-side slippage.",
                             {slip: grid[(m, short, slip)][2] for slip in SLIPS}, curve, log, hold["SPY"])
    curve, log, _ = old_capped[(5, True, BASE_SLIP)]
    write_run_folder(HERE / "old-5min-top20-capped", "intraday-orb-old-5min-top20-capped",
                     "The old strategies/intraday/orb setup (5-minute range, long-short, monthly top 20 by dollar volume from "
                     "intraday.CANDIDATES) re-run with each position capped at equity / 20, so gross never exceeds equity. "
                     "Compare with strategies/intraday/orb (uncapped, up to 4x).",
                     {slip: old_capped[(5, True, slip)][2] for slip in SLIPS}, curve, log, hold["SPY"])
    print("done", round(time.time() - started), "s")


if __name__ == "__main__":
    main()

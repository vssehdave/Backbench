"""Standard run output: results/report.json, REPORT.md and trade logs for the best, worst and a random day.

One adapter per engine turns its result into folds of {label, dates, equity, bench, fills, borrow}; everything
after that is shared. equity and bench hold one more point than dates (the opening value first).
"""
import csv
import json
import random
from pathlib import Path

COLUMNS = ["fold", "date", "when", "symbol", "side", "quantity", "price", "fees", "reason",
           "position_before", "position_after"]


def _fill(f, engine, state):
    """One normalized fill. state is {symbol: position} and is updated in place."""
    symbol = f.get("symbol", "position")
    if engine == "harness":
        before = state.get(symbol, 0)
        after = before + f["quantity"]
        side = "buy" if f["quantity"] > 0 else "sell"
        reason = "margin call: flattened at the close" if f.get("forced") else f"target position {after} shares"
        fees, when, qty = f["commission"] + f["regulatory"], "close" if f.get("forced") else "open", f["quantity"]
    elif engine == "xsection":
        before, after, side, qty = f["position_before"], f["position_after"], f["side"], f["quantity"]
        fees, when, reason = f["commission"] + f["regulatory"] + f["slippage"], "close", f["reason"]
    else:
        before, after, side, qty = f["position_before"], f["position_after"], f["side"], f["quantity"]
        fees, when, reason = f["fee"], "close", f["reason"]
    state[symbol] = after
    return dict(date=f["date"], when=when, symbol=symbol, side=side, quantity=qty, price=f["price"], fees=fees,
                reason=reason, position_before=before, position_after=after)


def folds_of(engine, result, bench=None):
    """Normalize an engine result. bench is a second result of the same engine (harness only)."""
    if engine == "options":
        d = result["daily"]
        return [dict(label="full period", dates=d["dates"][1:], equity=d["equity"], bench=d["buy_and_hold"],
                     fills=result["fills"], borrow={})]
    out = []
    for i, f in enumerate(result["folds"]):
        if engine == "harness":
            other = bench["folds"][i]["equity"]
            symbol = result["config"]["symbol"]
            out.append(dict(label=f["forward_start"], dates=f["dates"], equity=[10000.] + f["equity"],
                            bench=[10000.] + other, fills=[dict(t, symbol=symbol) for t in f["fills"]],
                            borrow=f["borrow"]))
        else:
            b = f["bench_equity"].get("spy") or f["bench_equity"]["equal_weight_universe"]
            borrow = {d: x for d, x in zip(f["dates"], f["borrow_daily"]) if x}
            out.append(dict(label=f["test_start"], dates=f["dates"][1:], equity=f["equity"], bench=b,
                            fills=f["fills"], borrow=borrow))
    return out


def ledger(folds, engine):
    """(days, fills). A day is one session's P&L; fills carry the fold and running position."""
    days, fills = [], []
    for n, fold in enumerate(folds):
        state, by_day = {}, {}
        for f in fold["fills"]:
            by_day.setdefault(f["date"], []).append(f)
        for k, day in enumerate(fold["dates"]):
            before = {s: p for s, p in state.items() if p}
            today = []
            for f in by_day.get(day, []):
                row = _fill(f, engine, state)
                row["fold"] = fold["label"]
                today.append(row)
            e0, e1, b0, b1 = fold["equity"][k], fold["equity"][k + 1], fold["bench"][k], fold["bench"][k + 1]
            days.append(dict(fold=fold["label"], date=day, pnl=e1 - e0, ret=e1 / e0 - 1 if e0 else 0.,
                             bench_ret=b1 / b0 - 1 if b0 else 0., borrow=fold["borrow"].get(day, 0.),
                             before=before, after={s: p for s, p in state.items() if p}, fills=today))
            fills.extend(today)
    return days, fills


def pick_days(days, seed):
    traded = [d for d in days if d["fills"]]
    if not days or not traded:
        raise ValueError("The run has no session with a fill to show")
    return dict(best=max(days, key=lambda d: d["pnl"]), worst=min(days, key=lambda d: d["pnl"]),
                random=random.Random(seed).choice(traded))


def _positions(p):
    return ", ".join(f"{s} {v:+,.4g}" for s, v in sorted(p.items())) or "flat"


def day_md(title, d):
    lines = [f"# {title}: {d['date']} (fold {d['fold']})", "",
             f"- Strategy P&L: {d['pnl']:+,.2f} USD ({d['ret']:+.3%})",
             f"- Benchmark move that day: {d['bench_ret']:+.3%}",
             f"- Borrow charged: {d['borrow']:,.4f} USD",
             f"- Position before: {_positions(d['before'])}", f"- Position after: {_positions(d['after'])}", ""]
    if not d["fills"]:
        return "\n".join(lines + ["No fills that day."]) + "\n"
    lines += ["| when | symbol | side | quantity | price | fees USD | position before | position after | reason |",
              "|---|---|---|---|---|---|---|---|---|"]
    lines += [f"| {f['date']} {f['when']} | {f['symbol']} | {f['side']} | {f['quantity']:,.4g} | {f['price']:,.4f} | "
              f"{f['fees']:,.4f} | {f['position_before']:,.4g} | {f['position_after']:,.4g} | {f['reason']} |"
              for f in d["fills"]]
    return "\n".join(lines) + "\n"


def write_csv(path, rows, extra=()):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS + list(extra), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _pct(x):
    return "n/a" if x is None else f"{x:.1%}"


def mc_table(name, mc):
    d, h = mc["max_drawdown"], mc["historical"]
    ex = d["prob_exceed"]
    return (f"| {name} | {h['max_drawdown']:.1%} ({d['historical_percentile_rank']:.0f}th pct) | "
            f"{d['p5']:.1%} | {d['p50']:.1%} | {d['p95']:.1%} | {d['p99']:.1%} | "
            f"{ex['0.2']:.1%} / {ex['0.3']:.1%} / {ex['0.5']:.1%} | "
            f"{mc['longest_underwater_sessions']['p50']:.0f} / {mc['longest_underwater_sessions']['p95']:.0f} | "
            f"{mc['terminal_return']['p5']:.1%} / {mc['terminal_return']['p50']:.1%} / {mc['terminal_return']['p95']:.1%} |")


MC_HEAD = ["| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | "
           "underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |", "|---|---|---|---|---|---|---|---|---|"]


def write_report(out_dir, engine, name, result, mc, folds, seed=0, extra=None):
    """Write the whole result folder. mc maps series name -> montecarlo summary dict (strategy first)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    days, fills = ledger(folds, engine)
    picks = pick_days(days, seed)
    report = dict(name=name, engine=engine, result=result, monte_carlo=mc, **(extra or {}))
    (out / "report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    write_csv(out / "trades_all.csv", fills)
    for key, d in picks.items():
        (out / f"trades_{key}_day.md").write_text(day_md(f"{key.capitalize()} day", d), encoding="utf-8")
        write_csv(out / f"trades_{key}_day.csv", d["fills"])
    md = [f"# {name}", "", "## Monte Carlo max drawdown", ""] + MC_HEAD + [mc_table(k, v) for k, v in mc.items()]
    md += ["", "## Walk-forward folds", "", "| fold | return | benchmark | max DD | fills |", "|---|---|---|---|---|"]
    for f in folds:
        e, b = f["equity"], f["bench"]
        peak, dd = e[0], 0.
        for v in e:
            peak = max(peak, v)
            dd = min(dd, v / peak - 1)
        md.append(f"| {f['label']} | {e[-1] / e[0] - 1:.2%} | {b[-1] / b[0] - 1:.2%} | {dd:.1%} | {len(f['fills'])} |")
    md += ["", "Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail "
           "(Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.",
           ""]
    (out / "REPORT.md").write_text("\n".join(md), encoding="utf-8")
    return picks

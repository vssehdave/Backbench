"""Standard run output: results/report.json, REPORT.md and trade logs for the best, worst and a random day.

One adapter per engine turns its result into folds of {label, dates, equity, bench, fills, borrow}; everything
after that is shared. equity and bench hold one more point than dates (the opening value first).
"""
import csv
import json
import math
import random
import statistics
from bisect import bisect_right
from datetime import date
from pathlib import Path

COLUMNS = ["fold", "date", "when", "symbol", "side", "quantity", "price", "fees", "reason",
           "position_before", "position_after"]


def _fill(f, engine, state):
    """One normalized fill. state is {symbol: position} and is updated in place."""
    symbol = f.get("symbol", "position")
    if engine in ("harness", "multi"):
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
                     fills=result["fills"], borrow={}, bench_name="underlying buy and hold")]
    out = []
    for i, f in enumerate(result["folds"]):
        if engine == "harness":  # its buy_and_hold control keeps part of the cash, so it is not the SPY row
            other = bench["folds"][i]["equity"]
            symbol = result["config"]["symbol"]
            out.append(dict(label=f["forward_start"], dates=f["dates"], equity=[10000.] + f["equity"],
                            bench=[10000.] + other, fills=[dict(t, symbol=symbol) for t in f["fills"]],
                            borrow=f["borrow"], bench_name="benchmark (harness buy and hold, part cash)"))
        elif engine == "multi":
            # Weight 1.0 is half the cash, so the benchmark is not plain SPY; beta and alpha need the spy closes.
            units = ", ".join(f"{s} {w:g}" for s, w in result["manifest"]["benchmark"].items())
            out.append(dict(label=f["forward_start"], dates=f["dates"], equity=[10000.] + f["equity"],
                            bench=[10000.] + f["bench_equity"], fills=f["fills"], borrow={},
                            bench_name=f"benchmark ({units} unit)"))
        else:
            b = f["bench_equity"].get("spy") or f["bench_equity"]["equal_weight_universe"]
            name = "SPY" if f["bench_equity"].get("spy") else "equal-weight universe"
            borrow = {d: x for d, x in zip(f["dates"], f["borrow_daily"]) if x}
            out.append(dict(label=f["test_start"], dates=f["dates"][1:], equity=f["equity"], bench=b,
                            fills=f["fills"], borrow=borrow, bench_name=name))
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
            days.append(dict(fold=fold["label"], date=day, bench_name=fold.get("bench_name", "benchmark"), pnl=e1 - e0, ret=e1 / e0 - 1 if e0 else 0.,
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


def perf_metrics(returns, bench=None, periods=252, years=None):
    """The one metrics function. returns and bench (SPY, same sessions) are per-session simple returns.

    Risk-free rate is 0. Sortino divides the mean by downside deviation below 0 taken over all sessions. Beta is the OLS
    slope of returns on bench; alpha is the annualized intercept, (mean(r) - beta * mean(b)) * periods.
    years defaults to sessions / periods.
    """
    n = len(returns)
    mean = statistics.fmean(returns) if n else 0.
    sd = statistics.stdev(returns) if n > 1 else 0.
    down = math.sqrt(sum(min(r, 0.) ** 2 for r in returns) / n) if n else 0.
    equity = peak = 1.
    dd = 0.
    for r in returns:
        equity *= 1 + r
        peak = max(peak, equity)
        dd = min(dd, equity / peak - 1)
    years = years or n / periods
    out = dict(total_return=equity - 1, cagr=equity ** (1 / years) - 1 if equity > 0 and years else None,
               volatility=sd * math.sqrt(periods), sharpe=mean / sd * math.sqrt(periods) if sd else None,
               sortino=mean / down * math.sqrt(periods) if down else None, max_drawdown=dd, beta=None, alpha=None)
    if bench is not None and n > 1:
        mb = statistics.fmean(bench)
        var = sum((b - mb) ** 2 for b in bench)
        if var:
            out["beta"] = sum((b - mb) * (r - mean) for r, b in zip(returns, bench)) / var
            out["alpha"] = (mean - out["beta"] * mb) * periods
    return out


def _day(d):
    return d if isinstance(d, date) else date.fromisoformat(str(d))


def spy_returns(dates, spy):
    """Per-session SPY return for each date from a {date: close} map; 0 on a date SPY has no close for."""
    keys = sorted(spy)
    out = []
    for d in map(_day, dates):
        i = bisect_right(keys, d)
        out.append(spy[keys[i - 1]] / spy[keys[i - 2]] - 1 if i >= 2 and keys[i - 1] == d else 0.)
    return out


def standard_metrics(days, spy=None, periods=252):
    """{series name: perf_metrics} for the chained sessions of a run: strategy, its own benchmark, and SPY if different.

    Beta and alpha are always against SPY: from spy ({date: close}) if given, else from the benchmark when that is SPY,
    else left empty.
    """
    r, b, bn = [d["ret"] for d in days], [d["bench_ret"] for d in days], days[0]["bench_name"]
    s = spy_returns([d["date"] for d in days], spy) if spy else (b if bn == "SPY" else None)
    out = {"strategy": perf_metrics(r, s, periods), bn: perf_metrics(b, s, periods)}
    if s is not None and bn != "SPY":
        out["SPY"] = perf_metrics(s, s, periods)
    return out


def curves(days):
    """(dates, {strategy, benchmark: growth of 10,000}, {same: drawdown}) chaining the sessions' returns."""
    dates = [_day(days[0]["date"])] + [_day(d["date"]) for d in days]
    names = {"ret": "strategy", "bench_ret": days[0]["bench_name"]}
    grow, down = {}, {}
    for key, label in names.items():
        v = peak = 10000.
        grow[label], down[label] = [v], [0.]
        for d in days:
            v *= 1 + d[key]
            peak = max(peak, v)
            grow[label].append(v)
            down[label].append(v / peak - 1)
    return dates, grow, down


def equity_svg(dates, series, drawdowns, width=900):
    """Standard-library SVG: growth of 10,000 on a log axis over a drawdown strip, one colour per series.

    One point per date; the x axis is the session index, so any gap between walk-forward windows is not drawn.
    """
    n, left, right, h1, h2, top1 = len(dates), 60, 20, 300, 90, 30
    top2 = top1 + h1 + 30
    lo = math.log(min(min(v) for v in series.values()))
    hi = max(math.log(max(max(v) for v in series.values())), lo + 1e-9)
    floor = min(-0.05, min(min(v) for v in drawdowns.values()))
    x = lambda i: left + (width - left - right) * i / max(n - 1, 1)
    y1 = lambda v: top1 + h1 * (1 - (math.log(v) - lo) / (hi - lo))
    y2 = lambda v: top2 + h2 * v / floor
    colors = ["#1f4e9c", "#8a8a8a"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{top2 + h2 + 30}" font-family="sans-serif" '
         f'font-size="11"><rect width="100%" height="100%" fill="white"/>']
    for k in range(5):  # gridlines evenly spaced in log space
        v = math.exp(lo + (hi - lo) * k / 4)
        o.append(f'<line x1="{left}" x2="{width - right}" y1="{y1(v):.1f}" y2="{y1(v):.1f}" stroke="#e5e5e5"/>'
                 f'<text x="{left - 5}" y="{y1(v) + 4:.1f}" text-anchor="end">{v:,.0f}</text>')
    firsts = [i for i in range(n) if i == 0 or dates[i].year != dates[i - 1].year]
    for i in firsts[::max(1, math.ceil(len(firsts) / 12))]:
        o.append(f'<line x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{top1}" y2="{top2 + h2}" stroke="#f0f0f0"/>'
                 f'<text x="{x(i):.1f}" y="{top2 + h2 + 15}" text-anchor="middle">{dates[i].year}</text>')
    for vals, c in zip(series.values(), colors):
        o.append(f'<polyline points="{" ".join(f"{x(i):.1f},{y1(v):.1f}" for i, v in enumerate(vals))}" fill="none" '
                 f'stroke="{c}" stroke-width="1.5"/>')
    for vals, c in reversed(list(zip(drawdowns.values(), colors))):
        pts = " ".join(f"{x(i):.1f},{y2(v):.1f}" for i, v in enumerate(vals))
        o.append(f'<polygon points="{x(0):.1f},{y2(0):.1f} {pts} {x(n - 1):.1f},{y2(0):.1f}" fill="{c}" '
                 f'fill-opacity="0.3" stroke="{c}"/>')
    o.append(f'<text x="{left - 5}" y="{y2(0) + 4:.1f}" text-anchor="end">0%</text>'
             f'<text x="{left - 5}" y="{y2(floor) + 4:.1f}" text-anchor="end">{floor:.0%}</text>'
             f'<text x="{left}" y="18" font-size="13">Growth of 10,000 (log scale), drawdown below: '
             + ", ".join(f'<tspan fill="{c}">{k}</tspan>' for k, c in zip(series, colors)) + "</text></svg>")
    return "\n".join(o)


def _num(x, fmt):
    return "n/a" if x is None else format(x, fmt)


METRIC_HEAD = ["| series | CAGR | Sharpe | Sortino | volatility | max DD | beta vs SPY | alpha vs SPY (annual) |",
               "|---|---|---|---|---|---|---|---|"]


def metric_row(name, m):
    return (f"| {name} | {_num(m['cagr'], '.1%')} | {_num(m['sharpe'], '.2f')} | {_num(m['sortino'], '.2f')} | "
            f"{m['volatility']:.1%} | {m['max_drawdown']:.1%} | {_num(m['beta'], '.2f')} | {_num(m['alpha'], '+.1%')} |")


def without_fills(x):
    """Copy of x with every list under a "fills" key replaced by its length (the fills are in trades_all.csv)."""
    if isinstance(x, dict):
        return {k: len(v) if k == "fills" and isinstance(v, list) else without_fills(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [without_fills(v) for v in x]
    return x


def write_report(out_dir, engine, name, result, mc, folds, seed=0, extra=None, spy=None, periods=252):
    """Write the whole result folder. mc maps series name -> montecarlo summary dict (strategy first).

    spy is an optional {date: close} map for beta and alpha when the engine's own benchmark is not SPY. periods is
    sessions per year (365 for a 24/7 market).
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    days, fills = ledger(folds, engine)
    picks = pick_days(days, seed)
    metrics = standard_metrics(days, spy, periods)
    (out / "equity.svg").write_text(equity_svg(*curves(days)), encoding="utf-8")
    report = dict(name=name, engine=engine, fills=len(fills), metrics=metrics, result=without_fills(result), monte_carlo=mc,
                  **(extra or {}))
    (out / "report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    write_csv(out / "trades_all.csv", fills)
    for key, d in picks.items():
        (out / f"trades_{key}_day.md").write_text(day_md(f"{key.capitalize()} day", d), encoding="utf-8")
        write_csv(out / f"trades_{key}_day.csv", d["fills"])
    c = (extra or {}).get("mc_config", {})
    md = [f"# {name}", "", "![Growth of 10,000 and drawdown](equity.svg)", "", "## Performance", "",
          f"{days[0]['date']} to {days[-1]['date']}, {len(days)} sessions chained, zero risk-free rate, {periods} sessions a year "
          "(CAGR from the session count). Sortino uses downside deviation below 0. Beta and annualized alpha are a CAPM "
          "regression of daily returns on SPY, whatever the headline benchmark.", ""] + METRIC_HEAD          + [metric_row(k, v) for k, v in metrics.items()] + ["", "## Monte Carlo max drawdown", "",
          f"{c.get('mode', '')}; {c.get('paths', '')} paths, seed {c.get('seed', '')}, mean block {c.get('mean_block', '')}. "
          f"{c.get('note', '')}", ""] + MC_HEAD + [mc_table(k, v) for k, v in mc.items()]
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

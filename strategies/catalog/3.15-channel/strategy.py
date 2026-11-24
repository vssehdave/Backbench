"""Paper 3.15, long-only Donchian channel on closes: buy at the T-day floor, liquidate at the ceiling, else hold."""


def decide(history, level):
    t = int(level)
    window, price = history[-t - 1:-1], history[-1]
    if price <= min(window):
        return int(5000 / history[0])
    return 0 if price >= max(window) else None

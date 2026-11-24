"""Paper 3.11, long-only: long when the close is above its T-day simple moving average, flat when below."""


def decide(history, level):
    t = int(level)
    price, ma = history[-1], sum(history[-t:]) / t
    if price == ma:
        return None
    return int(5000 / history[0]) if price > ma else 0

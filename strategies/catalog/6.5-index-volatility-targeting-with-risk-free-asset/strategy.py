"""Paper 6.5 with stated approximations: weight = target vol / 20-day realised vol, capped at 1 and floored to
quarter steps (decide has no state for the paper's rebalance threshold). Cash earns 0%. level = annual target vol."""
WINDOW = 20


def decide(history, level):
    r = [b / a - 1 for a, b in zip(history[-WINDOW - 1:-1], history[-WINDOW:])]
    mean = sum(r) / WINDOW
    vol = (sum((x - mean) ** 2 for x in r) / (WINDOW - 1)) ** 0.5 * 252 ** 0.5
    weight = min(1., level / vol) if vol else 1.
    return int(int(weight * 4) / 4 * int(5000 / history[0]))

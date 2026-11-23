"""Deterministic controls. No investment hypotheses."""
def threshold(history, level):
    """Target ten whole shares above the threshold, otherwise cash."""
    return 10 if history[-1] > level else 0


def cash(history, level):
    return 0

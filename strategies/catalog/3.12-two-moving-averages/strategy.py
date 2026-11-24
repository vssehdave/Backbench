"""Paper 3.12, long-only, without the stop-loss variant: long when MA(10) > MA(T), flat when below. level = T."""
FAST = 10


def decide(history, level):
    t = int(level)
    fast, slow = sum(history[-FAST:]) / FAST, sum(history[-t:]) / t
    if fast == slow:
        return None
    return int(5000 / history[0]) if fast > slow else 0

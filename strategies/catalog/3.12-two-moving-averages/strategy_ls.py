"""Paper 3.12, long/short, without the stop-loss variant: long when MA(10) > MA(T), short when below. level = T."""
FAST = 10


def decide(history, level):
    t = int(level)
    fast, slow = sum(history[-FAST:]) / FAST, sum(history[-t:]) / t
    if fast == slow:
        return None
    size = int(5000 / history[0])
    return size if fast > slow else -size

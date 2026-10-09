"""Forgetting is prior best score minus current retained score."""
def forgetting(best: float,current: float) -> float:
    return max(0.0,best-current)

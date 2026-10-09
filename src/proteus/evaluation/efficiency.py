"""Successful tasks per compute-second."""
def throughput(successes: int,seconds: float) -> float:
    return successes/max(1e-9,seconds)

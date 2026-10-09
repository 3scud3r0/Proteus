"""Return and discounted return utilities."""
def discounted_return(rewards: list[float], gamma: float = 0.99) -> float:
    value=0.0
    for r in reversed(rewards):
        value=float(r)+gamma*value
    return value

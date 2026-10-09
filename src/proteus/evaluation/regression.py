"""Prevent selecting an improvement that breaks protected metrics."""
def acceptable(candidate: dict[str,float],baseline: dict[str,float],tolerance: float = 0.02) -> bool:
    return all(candidate.get(k,float("-inf"))>=v-tolerance for k,v in baseline.items())

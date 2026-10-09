"""Identify measured below-target capabilities."""
def detect(scores: dict[str,float],targets: dict[str,float]) -> list[str]:
    return sorted(k for k,target in targets.items() if scores.get(k,float("-inf"))<target)

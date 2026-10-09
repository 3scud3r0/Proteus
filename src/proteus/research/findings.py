"""Outcome labels do not claim scientific novelty."""
def interpret(effect: float,threshold: float = 0.01) -> str:
    return "improved" if effect>threshold else "regressed" if effect<-threshold else "inconclusive"

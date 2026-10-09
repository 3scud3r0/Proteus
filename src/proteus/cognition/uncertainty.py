"""Simple probability-vector uncertainty measures."""
import math

def entropy(probabilities: list[float]) -> float:
    if any(p<0 for p in probabilities) or abs(sum(probabilities)-1)>1e-6:
        raise ValueError("Expected probability distribution")
    return -sum(p*math.log2(p) for p in probabilities if p>0)

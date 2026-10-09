"""Normalized set novelty of observed signatures."""
def novelty(signature: set, prior: set) -> float:
    return len(signature-prior)/max(1,len(signature | prior))

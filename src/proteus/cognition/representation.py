"""Normalized features for simple downstream predictive models."""
from proteus.core.protocols import State

def encode(state: State, size: int) -> tuple[float,...]:
    if size<2: raise ValueError("size must be >=2")
    return tuple(v/(size-1) for v in state)

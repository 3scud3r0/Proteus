"""Aggregate episode statistics from recorded transitions."""
from proteus.core.protocols import Transition

def summarize(transitions: list[Transition]) -> dict:
    if not transitions:
        return {"count": 0, "reward": 0.0, "terminal": 0}
    return {"count": len(transitions), "reward": sum(t.reward for t in transitions), "terminal": sum(t.done for t in transitions)}

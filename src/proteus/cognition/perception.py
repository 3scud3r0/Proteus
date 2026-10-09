"""Validate observations before use by downstream components."""
from proteus.core.protocols import State

def perceive(raw: object) -> State:
    if not isinstance(raw,(tuple,list)) or len(raw)!=4 or any(type(v) is not int for v in raw):
        raise ValueError("Expected (x,y,goal_x,goal_y) integer observation")
    return tuple(raw)

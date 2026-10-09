"""Prediction targets are obtained from observed transitions."""
from proteus.core.protocols import Transition

def transition_target(t: Transition) -> tuple:
    return t.next_state

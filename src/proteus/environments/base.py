"""Environment result standardization."""
from dataclasses import dataclass
from proteus.core.protocols import State

@dataclass(frozen=True)
class Step:
    observation: State
    reward: float
    terminal: bool
    info: dict

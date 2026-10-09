"""Small stable contracts between modules (no framework dependency)."""
from dataclasses import dataclass, field
from typing import Any, Protocol

State = tuple[int, int, int, int]

@dataclass(frozen=True)
class Transition:
    state: State
    action: int
    reward: float
    next_state: State
    done: bool
    episode: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

class Environment(Protocol):
    actions: tuple[int, ...]
    def reset(self, seed: int | None = None) -> State: ...
    def step(self, action: int) -> tuple[State, float, bool, dict[str, Any]]: ...

class Learner(Protocol):
    def select_action(self, state: State, training: bool = True) -> int: ...
    def learn(self, transition: Transition) -> float: ...

"""Enforces episode and wall-clock budgets; GPU is not required."""
import time
from dataclasses import dataclass

@dataclass(frozen=True)
class Budget:
    max_seconds: float = 30.0
    max_episodes: int = 500

class ResourceManager:
    def __init__(self, budget: Budget):
        self.budget = budget
        self.started = time.monotonic()
        self.completed = 0
    def allowed(self) -> bool:
        return self.completed < self.budget.max_episodes and (time.monotonic() - self.started) < self.budget.max_seconds
    def record_episode(self) -> None:
        self.completed += 1

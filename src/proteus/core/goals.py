"""Persistent-friendly goal records with measurable targets."""
from dataclasses import dataclass

@dataclass
class Goal:
    name: str
    metric: str
    target: float
    priority: int = 0
    enabled: bool = True
    def achieved(self, measurements: dict[str, float]) -> bool:
        return self.enabled and measurements.get(self.metric, float("-inf")) >= self.target

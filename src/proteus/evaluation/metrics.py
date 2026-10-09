"""Holdout aggregate metrics."""
from dataclasses import dataclass,asdict

@dataclass(frozen=True)
class Scores:
    episodes: int
    success_rate: float
    mean_return: float
    mean_steps: float
    def to_dict(self):return asdict(self)

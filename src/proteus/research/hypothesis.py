"""Testable hypothesis definition."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Hypothesis:
    claim: str
    metric: str
    minimum_effect: float

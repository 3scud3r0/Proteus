"""Minimal immutable evidence references."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    source: str
    experiment_id: str
    verified: bool = False

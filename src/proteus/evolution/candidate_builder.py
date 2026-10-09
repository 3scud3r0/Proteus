"""Immutable hyperparameter candidate identity."""
from dataclasses import dataclass
from proteus.research.reproducibility import fingerprint

@dataclass(frozen=True)
class Candidate:
    id: str
    settings: dict

def build(settings: dict) -> Candidate:
    return Candidate(fingerprint(settings)[:16],dict(settings))

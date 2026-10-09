"""Dependency graph used to explain prerequisites for skills."""
from collections import defaultdict

class CapabilityGraph:
    def __init__(self):self.requires=defaultdict(set)
    def add(self,skill: str,prerequisites: set[str] | None = None) -> None:
        self.requires[skill].update(prerequisites or set())
    def available(self,known: set[str]) -> set[str]:
        return {name for name,dependencies in self.requires.items() if dependencies<=known}

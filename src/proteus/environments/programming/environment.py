"""Programming-task description; code execution is separately permissioned."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ProgrammingTask:
    name: str
    specification: str
    tests: tuple[tuple[tuple, object], ...]

"""Explicit lifecycle; restart recovery is provided by state and checkpoint files."""
from dataclasses import dataclass
from enum import Enum

class Phase(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"

@dataclass
class Lifecycle:
    phase: Phase = Phase.STOPPED
    def start(self) -> None:
        if self.phase == Phase.RUNNING:
            raise RuntimeError("Already running")
        self.phase = Phase.RUNNING
    def pause(self) -> None:
        if self.phase != Phase.RUNNING:
            raise RuntimeError("Not running")
        self.phase = Phase.PAUSED
    def stop(self) -> None:
        self.phase = Phase.STOPPED

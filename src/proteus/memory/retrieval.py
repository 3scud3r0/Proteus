"""Retrieve most recent matching transition from persisted memory."""
from proteus.memory.episodic import EpisodicMemory

def matching_state(memory: EpisodicMemory, state: tuple, limit: int = 500):
    return [t for t in memory.recent(limit) if t.state == state]

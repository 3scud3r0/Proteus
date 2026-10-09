"""Bounded uniform experience replay using an isolated RNG."""
from collections import deque
import random
from proteus.core.protocols import Transition

class ReplayBuffer:
    def __init__(self, capacity: int = 1500, seed: int = 7):
        if capacity < 1: raise ValueError("Capacity must be positive")
        self.values: deque[Transition] = deque(maxlen=capacity)
        self.rng = random.Random(seed)
    def add(self, transition: Transition) -> None:
        self.values.append(transition)
    def sample(self, size: int) -> list[Transition]:
        return self.rng.sample(list(self.values),min(max(0,size),len(self.values)))
    def __len__(self):
        return len(self.values)

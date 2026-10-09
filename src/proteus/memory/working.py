"""Bounded short-term observation cache."""
from collections import deque

class WorkingMemory:
    def __init__(self, capacity: int = 64):
        self.items: deque = deque(maxlen=capacity)
    def add(self, item: object) -> None:
        self.items.append(item)
    def read(self) -> list:
        return list(self.items)

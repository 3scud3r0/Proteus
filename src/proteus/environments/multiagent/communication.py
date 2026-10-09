"""Local in-memory, non-networked message passing."""
from collections import defaultdict, deque

class MessageChannel:
    def __init__(self, capacity: int = 100):
        self.boxes=defaultdict(lambda:deque(maxlen=capacity))
    def send(self, recipient: str, message: dict) -> None:
        self.boxes[recipient].append(dict(message))
    def receive(self, recipient: str) -> list[dict]:
        values=list(self.boxes[recipient]); self.boxes[recipient].clear()
        return values

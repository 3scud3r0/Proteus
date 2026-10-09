"""Independent toy agents sharing a message channel."""
from proteus.environments.multiagent.communication import MessageChannel

class MultiAgentWorld:
    def __init__(self, names: list[str]):
        self.names=tuple(names)
        self.messages=MessageChannel()
    def broadcast(self, sender: str, payload: dict) -> None:
        if sender not in self.names: raise ValueError("Unknown sender")
        for n in self.names:
            if n!=sender: self.messages.send(n,{"sender":sender,"payload":payload})

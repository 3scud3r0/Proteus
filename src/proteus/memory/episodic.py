"""Append-only experience persistence."""
import json
from proteus.core.protocols import Transition
from proteus.infrastructure.database import Database

class EpisodicMemory:
    def __init__(self, db: Database):
        self.db = db
    def add(self, transition: Transition) -> None:
        self.db.execute("INSERT INTO experiences(state,action,reward,next_state,done,episode,metadata) VALUES(?,?,?,?,?,?,?)", (
            json.dumps(transition.state), transition.action, transition.reward,
            json.dumps(transition.next_state), int(transition.done), transition.episode,
            json.dumps(transition.metadata)))
    def recent(self, limit: int = 100) -> list[Transition]:
        limit = max(0, min(int(limit), 10000))
        rows = self.db.rows("SELECT state,action,reward,next_state,done,episode,metadata FROM experiences ORDER BY id DESC LIMIT ?", (limit,))
        return [Transition(tuple(json.loads(s)), a, r, tuple(json.loads(ns)), bool(done), e, json.loads(m)) for s,a,r,ns,done,e,m in rows]
    def __len__(self):
        return self.db.count("experiences")

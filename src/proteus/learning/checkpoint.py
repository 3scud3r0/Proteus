"""Persist and verify checksummed, non-executable model checkpoints."""
import hashlib
import json
from pathlib import Path
from proteus.core.state import StateStore
from proteus.learning.online_learner import OnlineQLearner

def save(learner: OnlineQLearner, path: Path) -> str:
    payload=learner.snapshot()
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":"))
    checksum=hashlib.sha256(canonical.encode()).hexdigest()
    StateStore(path).save({"payload":payload,"sha256":checksum,"format":1})
    return checksum

def load(learner: OnlineQLearner,path: Path) -> None:
    document=StateStore(path).load()
    if not document: return
    if document.get("format")!=1: raise ValueError("Unknown checkpoint format")
    canonical=json.dumps(document["payload"],sort_keys=True,separators=(",",":"))
    if hashlib.sha256(canonical.encode()).hexdigest()!=document["sha256"]:
        raise ValueError("Checkpoint checksum mismatch")
    learner.restore(document["payload"])

"""Restore previously recorded hyperparameter configuration."""
from proteus.core.state import StateStore

def restore(path) -> dict:
    value=StateStore(path).load()
    if not value:raise FileNotFoundError(path)
    return value["settings"]

"""Bound storage with an explicit retention policy."""
from proteus.infrastructure.database import Database

def prune_experiences(db: Database, keep_recent: int) -> int:
    if keep_recent < 0:
        raise ValueError("keep_recent must be nonnegative")
    count = db.count("experiences")
    n = max(0, count-keep_recent)
    if n:
        db.execute("DELETE FROM experiences WHERE id IN (SELECT id FROM experiences ORDER BY id LIMIT ?)", (n,))
    return n

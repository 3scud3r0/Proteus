"""Narrow telemetry API."""
from proteus.infrastructure.database import Database

def latest(db: Database,metric: str,limit: int = 10) -> list[float]:
    return [r[0] for r in db.rows("SELECT value FROM metrics WHERE metric=? ORDER BY id DESC LIMIT ?",(metric,min(1000,max(0,limit))))]

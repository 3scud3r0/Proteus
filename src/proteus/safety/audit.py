"""Durable record of decisions and sensitive attempted operations."""
import json
from proteus.infrastructure.database import Database

def log(db: Database,action: str,details: dict) -> None:
    db.execute("INSERT INTO audit(action,details) VALUES(?,?)",(action,json.dumps(details,ensure_ascii=False)))

"""Facts are explicitly labeled with provenance; no unverified auto-truths."""
import json
from typing import Any
from proteus.infrastructure.database import Database

class SemanticMemory:
    def __init__(self, db: Database):
        self.db = db
    def put(self, key: str, value: Any, provenance: str = "user") -> None:
        self.db.execute("INSERT INTO facts(key,value,provenance) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value,provenance=excluded.provenance,updated_at=CURRENT_TIMESTAMP", (key,json.dumps(value,ensure_ascii=False),provenance))
    def get(self, key: str) -> Any:
        rows = self.db.rows("SELECT value FROM facts WHERE key=?", (key,))
        return json.loads(rows[0][0]) if rows else None

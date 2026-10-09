"""Only validated procedures can be selected for future reuse."""
import json
from proteus.infrastructure.database import Database

class ProceduralMemory:
    def __init__(self, db: Database):
        self.db = db
    def save(self, name: str, procedure: dict, score: float, validated: bool = False) -> None:
        self.db.execute("INSERT INTO skills(name,procedure,score,validated) VALUES(?,?,?,?) ON CONFLICT(name) DO UPDATE SET procedure=excluded.procedure,score=excluded.score,validated=excluded.validated", (name,json.dumps(procedure),float(score),int(validated)))
    def validated(self) -> list[dict]:
        return [{"name":name,"procedure":json.loads(p),"score":score} for name,p,score in self.db.rows("SELECT name,procedure,score FROM skills WHERE validated=1 ORDER BY score DESC")]

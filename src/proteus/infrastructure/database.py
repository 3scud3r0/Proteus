"""SQLite persistence with explicit transactions; one DB per agent instance."""
import json
import sqlite3
from pathlib import Path
from threading import RLock
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS experiences (
 id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 state TEXT NOT NULL, action INTEGER NOT NULL, reward REAL NOT NULL,
 next_state TEXT NOT NULL, done INTEGER NOT NULL, episode INTEGER NOT NULL,
 metadata TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS facts (
 key TEXT PRIMARY KEY, value TEXT NOT NULL, provenance TEXT NOT NULL,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS skills (
 name TEXT PRIMARY KEY, procedure TEXT NOT NULL, score REAL NOT NULL,
 validated INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS metrics (
 id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 metric TEXT NOT NULL, value REAL NOT NULL, labels TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS experiments (
 id TEXT PRIMARY KEY, ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 hypothesis TEXT NOT NULL, config TEXT NOT NULL, results TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit (
 id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 action TEXT NOT NULL, details TEXT NOT NULL);
"""

class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.path), check_same_thread=False)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.lock = RLock()
        self.connection.executescript(SCHEMA)
        self.connection.commit()

    def execute(self, sql: str, parameters: tuple = ()) -> sqlite3.Cursor:
        with self.lock:
            cursor = self.connection.execute(sql, parameters)
            self.connection.commit()
            return cursor

    def rows(self, sql: str, parameters: tuple = ()) -> list[tuple]:
        with self.lock:
            return self.connection.execute(sql, parameters).fetchall()

    def count(self, table: str) -> int:
        if table not in {"experiences", "facts", "skills", "metrics", "experiments", "audit"}:
            raise ValueError("Invalid table")
        return int(self.rows(f"SELECT COUNT(*) FROM {table}")[0][0])

    def save_metric(self, name: str, value: float, labels: dict[str, Any] | None = None) -> None:
        self.execute("INSERT INTO metrics(metric,value,labels) VALUES(?,?,?)", (name, float(value), json.dumps(labels or {})))

    def close(self) -> None:
        with self.lock:
            self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

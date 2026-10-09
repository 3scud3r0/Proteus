"""Atomic SQLite backups, including databases using WAL."""
import sqlite3
from pathlib import Path
from proteus.infrastructure.database import Database

def backup(db: Database,destination: Path) -> Path:
    destination.parent.mkdir(parents=True,exist_ok=True)
    with db.lock,sqlite3.connect(str(destination)) as target:
        db.connection.backup(target)
    return destination

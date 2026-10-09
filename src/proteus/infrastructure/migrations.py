"""Schema migration entrypoint; version 1 is initialized by Database."""
from proteus.infrastructure.database import Database

def migrate(database: Database) -> int:
    database.execute("PRAGMA user_version = 1")
    return 1

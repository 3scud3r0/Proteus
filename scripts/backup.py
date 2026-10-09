"""Create a consistent SQLite backup from the default installation."""
from datetime import datetime,timezone
from proteus.infrastructure.database import Database
from proteus.infrastructure.backup import backup
from proteus.interface.cli import PROJECT
if __name__ == "__main__":
    path=PROJECT/"data"/"proteus.sqlite3"
    if not path.exists():raise SystemExit("Run `python -m proteus init` first")
    with Database(path) as db:
        dst=PROJECT/"data"/"backups"/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".sqlite3")
        backup(db,dst);print(dst)

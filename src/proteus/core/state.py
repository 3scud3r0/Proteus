"""Atomic JSON snapshots, never executable deserialization."""
import json
import os
from pathlib import Path
from typing import Any

class StateStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        obj = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError("State must be an object")
        return obj

    def save(self, value: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        with temp.open("w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, self.path)

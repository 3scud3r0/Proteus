"""Append NDJSON structured telemetry."""
import json
from pathlib import Path
from proteus.core.event_bus import Event

def append(path: Path,event: Event) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as f:
        f.write(json.dumps({"name":event.name,"timestamp":event.timestamp,"data":event.data},ensure_ascii=False)+"\n")

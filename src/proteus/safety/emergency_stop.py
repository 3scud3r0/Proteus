"""File-based external stop signal, checked between episodes."""
from pathlib import Path

class StopSignal:
    def __init__(self,path: Path):self.path=Path(path)
    def requested(self) -> bool:return self.path.exists()
    def request(self) -> None:
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.touch()
    def clear(self) -> None:self.path.unlink(missing_ok=True)

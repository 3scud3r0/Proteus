"""Filesystem confinement via resolved paths. NOT a process/OS sandbox."""
from pathlib import Path

class Workspace:
    def __init__(self,root: Path,max_bytes: int = 20_000_000):
        self.root=Path(root).resolve()
        self.root.mkdir(parents=True,exist_ok=True)
        self.max_bytes=max_bytes
    def path(self,relative: str) -> Path:
        requested=Path(relative)
        if requested.is_absolute():raise PermissionError("Absolute paths not allowed")
        full=(self.root/requested).resolve()
        if not full.is_relative_to(self.root) or full == self.root:
            raise PermissionError("Path leaves workspace or targets workspace root")
        return full
    def write(self,relative: str,content: str) -> Path:
        path=self.path(relative)
        size=len(content.encode("utf-8"))
        if size>self.max_bytes:raise ValueError("File exceeds workspace size limit")
        # Conservative total workspace quota, including the old version of the replaced file.
        existing=sum(p.stat().st_size for p in self.root.rglob("*") if p.is_file() and not p.is_symlink())
        old=path.stat().st_size if path.is_file() else 0
        if existing-old+size>self.max_bytes:raise ValueError("Workspace quota exceeded")
        path.parent.mkdir(parents=True,exist_ok=True)
        # Symlink ancestry is resolved during path(), and checked above.
        path.write_text(content,encoding="utf-8")
        return path
    def read(self,relative: str) -> str:
        path=self.path(relative)
        if path.stat().st_size>self.max_bytes:raise ValueError("File too large")
        return path.read_text(encoding="utf-8")

"""Content-addressed write-once experiment artifacts."""
from pathlib import Path
import hashlib

class ArtifactStore:
    def __init__(self,root: Path):self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
    def put(self,data: bytes) -> str:
        digest=hashlib.sha256(data).hexdigest()
        path=self.root/digest[:2]/digest
        path.parent.mkdir(parents=True,exist_ok=True)
        if not path.exists():path.write_bytes(data)
        return digest
    def get(self,digest: str) -> bytes:
        if len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):raise ValueError("Invalid digest")
        data=(self.root/digest[:2]/digest).read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:raise ValueError("Artifact integrity failure")
        return data

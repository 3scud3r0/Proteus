"""Workspace-only safe file operations."""
from proteus.safety.sandbox import Workspace

class FileTools:
    def __init__(self,workspace: Workspace):self.workspace=workspace
    def write(self,name: str,text: str) -> str:
        return str(self.workspace.write(name,text).relative_to(self.workspace.root))
    def read(self,name: str) -> str:
        return self.workspace.read(name)
    def list(self) -> list[str]:
        return sorted(str(p.relative_to(self.workspace.root)) for p in self.workspace.root.rglob("*") if p.is_file())

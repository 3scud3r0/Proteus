"""Tool capability allowlist."""
class ToolPermissions:
    def __init__(self,allowed: set[str] | None = None):self.allowed=allowed or set()
    def require(self,name: str) -> None:
        if name not in self.allowed:raise PermissionError(f"Tool not approved: {name}")

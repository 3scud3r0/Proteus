"""Unrestricted shell intentionally unavailable in the local prototype."""
def execute(command: str):
    raise PermissionError("Shell execution disabled; external isolation required")

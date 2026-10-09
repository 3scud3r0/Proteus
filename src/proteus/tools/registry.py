"""Register only intentionally exposed tool callables."""
from collections.abc import Callable

class ToolRegistry:
    def __init__(self):self._tools: dict[str,Callable]={}
    def register(self,name: str,fn: Callable) -> None:
        if name in self._tools:raise ValueError("Duplicate tool")
        self._tools[name]=fn
    def call(self,name: str,**kwargs):
        if name not in self._tools:raise PermissionError("Tool not registered")
        return self._tools[name](**kwargs)
    def list(self):return sorted(self._tools)

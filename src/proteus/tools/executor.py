"""Separates decision to use a tool from authorized execution."""
from proteus.tools.registry import ToolRegistry
from proteus.tools.permissions import ToolPermissions

class ToolExecutor:
    def __init__(self,registry: ToolRegistry,permissions: ToolPermissions):
        self.registry=registry;self.permissions=permissions
    def execute(self,name: str,**kwargs):
        self.permissions.require(name)
        return self.registry.call(name,**kwargs)

"""Create code as inert text inside the workspace; does not run it."""
import ast
from proteus.safety.sandbox import Workspace

def save_python(workspace: Workspace,name: str,source: str) -> str:
    if not name.endswith(".py"):raise ValueError("Expected .py file")
    ast.parse(source)
    return str(workspace.write(name,source))

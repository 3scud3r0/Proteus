"""Static syntax checks on code stored in the workspace."""
import ast
from proteus.safety.sandbox import Workspace

def syntax_check(workspace: Workspace,filename: str) -> dict:
    source=workspace.read(filename)
    try:
        ast.parse(source,filename=filename)
        return {"valid":True,"error":None}
    except SyntaxError as error:
        return {"valid":False,"error":f"line {error.lineno}: {error.msg}"}

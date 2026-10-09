"""Write validated JSON experiment products under workspace confinement."""
import json
from proteus.safety.sandbox import Workspace

def save_json(workspace: Workspace,name: str,data: dict) -> str:
    if not name.endswith(".json"):raise ValueError("Expected .json")
    return str(workspace.write(name,json.dumps(data,indent=2,ensure_ascii=False)))

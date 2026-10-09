"""Read-only Git metadata using an argument list (never shell=True)."""
import subprocess
from pathlib import Path

def status(repository: Path) -> str:
    proc=subprocess.run(["git","-C",str(Path(repository).resolve()),"status","--short"],
                        capture_output=True,text=True,timeout=5,check=False)
    if proc.returncode:raise RuntimeError(proc.stderr.strip()[:500])
    return proc.stdout[:10000]

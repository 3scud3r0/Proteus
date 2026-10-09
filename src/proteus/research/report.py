"""Pure Markdown reports with provenance and study limits."""
from pathlib import Path
import json

def write_report(path: Path,title: str,results: dict) -> Path:
    path.parent.mkdir(parents=True,exist_ok=True)
    text=f"# {title}\n\nResults from a bounded local experiment. No claim of general intelligence or scientific novelty.\n\n```json\n{json.dumps(results,indent=2,ensure_ascii=False)}\n```\n"
    path.write_text(text,encoding="utf-8")
    return path

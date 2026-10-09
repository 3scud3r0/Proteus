"""Offline text search in manually provided technical documents."""
from pathlib import Path

def find_text(root: Path,term: str,limit: int = 20) -> list[dict]:
    results=[]
    for path in sorted(Path(root).glob("*.md")):
        if path.stat().st_size>1_000_000:continue
        for i,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
            if term.casefold() in line.casefold():
                results.append({"file":path.name,"line":i,"text":line[:300]})
                if len(results)>=limit:return results
    return results

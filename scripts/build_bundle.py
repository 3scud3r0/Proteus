"""Concatenate all distributable text files into a single, attributed UTF-8 TXT."""
from hashlib import sha256
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT.parent
SKIP={"__pycache__",".pytest_cache",".git",".venv","data","runs","reports","proteus_research_agent.egg-info"}
SUFFIXES={".py",".toml",".md",".yaml",".example",".gitignore",".txt"}

def files():
    return sorted((p for p in ROOT.rglob("*") if p.is_file() and not any(x in SKIP for x in p.relative_to(ROOT).parts)
                  and (p.suffix in SUFFIXES or p.name in {".gitignore",".env.example"})),
                  key=lambda p:str(p.relative_to(ROOT)))

def build():
    selected=files()
    manifest=[]
    parts=["PROTEUS v0.1 | CÓDIGO FONTE COMPLETO CONSOLIDADO | UTF-8\n",
           "Este TXT é uma transcrição integral dos arquivos do projeto, não um binário compilado.\n",
           "Para executar, extraia o ZIP e leia README.md. Python é interpretado e foi validado com compileall.\n\n"]
    for p in selected:
        relative=p.relative_to(ROOT).as_posix()
        text=p.read_text(encoding="utf-8")
        digest=sha256(text.encode("utf-8")).hexdigest()
        manifest.append((relative,digest,text.count("\n")+int(not text.endswith("\n"))))
        parts += ["\n"+"="*100+"\n",f"ARQUIVO: {relative}\n",f"SHA256: {digest}\n","="*100+"\n",text,"\n"]
    parts.insert(3,"MANIFESTO:\n"+"\n".join(f"{name} | {lines} linhas | SHA256 {digest}" for name,digest,lines in manifest)+"\n")
    full="".join(parts)
    bundle=OUTPUT/"PROTEUS_CODIGO_COMPLETO.txt"
    bundle.write_text(full,encoding="utf-8")
    archive=OUTPUT/"PROTEUS_PROJETO_COMPLETO.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in selected:
            z.write(p,arcname="PROTEUS/"+p.relative_to(ROOT).as_posix())
    print(f"TXT: {bundle} ({bundle.stat().st_size:,} bytes)")
    print(f"ZIP: {archive} ({archive.stat().st_size:,} bytes)")
    print(f"FILES: {len(selected)}, PYTHON: {sum(p.suffix=='.py' for p in selected)}, LINES: {sum(x[2] for x in manifest)}")

if __name__=="__main__":build()

"""Small read-only HTML dashboard; user-generated values escaped."""
from html import escape

def render(status: dict) -> str:
    rows="".join(f"<tr><th>{escape(str(k))}</th><td>{escape(str(v))}</td></tr>" for k,v in status.items())
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>PROTEUS</title><style>body{{font:16px system-ui;margin:3rem auto;max-width:720px;padding:0 1rem;background:#111827;color:#e5e7eb}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #374151;padding:10px;text-align:left}}th{{color:#93c5fd}}</style></head><body><h1>PROTEUS</h1><p>Monitor local somente leitura. Atualize a página para ver dados recentes.</p><table>{rows}</table></body></html>'''

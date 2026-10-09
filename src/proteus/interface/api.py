"""Loopback-only read-only status API and dashboard, no CORS or side effects."""
import json
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from proteus.core.agent import ProteusAgent
from proteus.interface.dashboard import render

def serve(home: Path,port: int = 8765):
    if not 1024<=port<=65535:raise ValueError("Invalid port")
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/","/status","/health"):
                self.send_error(404);return
            if self.path == "/health":
                body=b'{"ok":true}';content_type="application/json"
            else:
                with ProteusAgent(home) as agent:status=agent.status()
                if self.path == "/status":
                    body=json.dumps(status,ensure_ascii=False).encode()
                    content_type="application/json"
                else:
                    body=render(status).encode();content_type="text/html; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type",content_type)
            self.send_header("X-Content-Type-Options","nosniff")
            self.send_header("Cache-Control","no-store")
            self.send_header("Content-Security-Policy","default-src 'none'; style-src 'unsafe-inline'")
            self.send_header("Content-Length",str(len(body)))
            self.end_headers();self.wfile.write(body)
    with HTTPServer(("127.0.0.1",port),Handler) as server:
        print(f"Local dashboard: http://127.0.0.1:{port}/")
        server.serve_forever()

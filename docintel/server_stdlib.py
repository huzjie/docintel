# -*- coding: utf-8 -*-
"""纯标准库 HTTP 服务（无 FastAPI 时的兜底）。"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from . import __version__
from .core.pipeline import Pipeline


def run_server(config: dict):
    pipe = Pipeline(config)
    host = config.get("server", {}).get("host", "127.0.0.1")
    port = config.get("server", {}).get("port", 8000)

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, obj):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/healthz", "/"):
                self._send(200, {"status": "ok", "version": __version__})
            elif self.path == "/formats":
                from .parsers.registry import list_parsers
                self._send(200, {"input": list_parsers()})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            if self.path == "/parse":
                length = int(self.headers.get("Content-Length", 0))
                data = self.rfile.read(length)
                # 简单处理：请求体当原始文档字节（multipart 需额外解析）
                filename = self.headers.get("X-Filename", "upload.bin")
                try:
                    result = pipe.run(data, source=filename)
                    self._send(200, {"summary": result.document.summary(),
                                     "text": result.document.text[:5000]})
                except Exception as e:
                    self._send(400, {"error": str(e)})
            else:
                self._send(404, {"error": "not found"})

        def log_message(self, *args):
            pass

    server = HTTPServer((host, port), Handler)
    print(f"docintel stdlib server on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


__all__ = ["run_server"]

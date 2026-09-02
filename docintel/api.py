# -*- coding: utf-8 -*-
"""FastAPI 控制面（惰性依赖 fastapi + uvicorn）。"""
from __future__ import annotations

import time
from typing import Dict

from . import __version__
from .core.pipeline import Pipeline
from .storage.store import DocStore


def create_app(config: Dict):
    from fastapi import FastAPI, File, HTTPException, UploadFile
    from fastapi.responses import JSONResponse

    app = FastAPI(title="docintel", version=__version__,
                  description="智能文档解析与结构化抽取平台")
    pipe = Pipeline(config)
    store = DocStore(config.get("storage", {}).get("path", ".docintel/data.db"))

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "version": __version__}

    @app.get("/")
    def root():
        return {"name": "docintel", "version": __version__,
                "docs": "/docs", "endpoints": ["/parse", "/formats", "/tasks"]}

    @app.get("/formats")
    def formats():
        from .parsers.registry import list_parsers
        return {"input": list_parsers(), "output": ["markdown", "json", "html", "csv"]}

    @app.post("/parse")
    async def parse(file: UploadFile = File(...), fmt: str = "json"):
        data = await file.read()
        store.record_task(file.filename, "running")
        t0 = time.time()
        try:
            result = pipe.run(data, source=file.filename, ext=file.filename.rsplit(".", 1)[-1])
            store.record_task(file.filename, "success",
                              elapsed_ms=int((time.time() - t0) * 1000))
            doc = result.document
            if fmt == "markdown":
                from .output.renderer import render
                return {"summary": doc.summary(), "markdown": render(doc, "markdown")}
            from .output.json_output import JsonRenderer
            return {"summary": doc.summary(), "data": __import__("json").loads(JsonRenderer().render(doc))}
        except Exception as e:
            store.record_task(file.filename, "failed", error=str(e))
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/tasks")
    def tasks():
        return {"tasks": store.recent_tasks(50)}

    return app


if __name__ == "__main__":
    import uvicorn
    from .config import load_config
    cfg = load_config()
    uvicorn.run(create_app(cfg), host=cfg.get("server", {}).get("host", "127.0.0.1"),
                port=cfg.get("server", {}).get("port", 8000))

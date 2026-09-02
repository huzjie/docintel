# -*- coding: utf-8 -*-
"""审计日志（追加 JSONL）。"""
from __future__ import annotations

import json
import time
from pathlib import Path


class AuditLog:
    def __init__(self, path: str = ".docintel/audit.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event: str, **kwargs) -> None:
        entry = {"ts": time.time(), "event": event, **kwargs}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


__all__ = ["AuditLog"]

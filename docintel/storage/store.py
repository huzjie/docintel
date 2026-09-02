# -*- coding: utf-8 -*-
"""SQLite 存储：保存解析结果与任务历史。"""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import closing
from pathlib import Path

from ..types import Document


class DocStore:
    def __init__(self, path: str = ".docintel/data.db"):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self):
        return sqlite3.connect(self.path)

    def _init(self):
        with closing(self._conn()) as c, c:
            c.execute("""CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT, format TEXT, title TEXT,
                summary TEXT, created_at REAL
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT, status TEXT, error TEXT,
                elapsed_ms INTEGER, created_at REAL
            )""")

    def save_document(self, doc: Document) -> int:
        with closing(self._conn()) as c, c:
            cur = c.execute(
                "INSERT INTO documents(source, format, title, summary, created_at) VALUES(?,?,?,?,?)",
                (doc.source, doc.format, doc.title, json.dumps(doc.summary(), ensure_ascii=False), time.time()),
            )
            return cur.lastrowid

    def record_task(self, source: str, status: str, error: str = "", elapsed_ms: int = 0) -> int:
        with closing(self._conn()) as c, c:
            cur = c.execute(
                "INSERT INTO tasks(source, status, error, elapsed_ms, created_at) VALUES(?,?,?,?,?)",
                (source, status, error, elapsed_ms, time.time()),
            )
            return cur.lastrowid

    def recent_tasks(self, limit: int = 50):
        with closing(self._conn()) as c, c:
            rows = c.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [{"id": r[0], "source": r[1], "status": r[2], "error": r[3],
                 "elapsed_ms": r[4], "created_at": r[5]} for r in rows]


__all__ = ["DocStore"]

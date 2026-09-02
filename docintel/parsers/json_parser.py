# -*- coding: utf-8 -*-
"""JSON 解析器。"""
from __future__ import annotations

import json

from ..types import Document
from .base import BaseParser


class JsonParser(BaseParser):
    extensions = ["json", "jsonl", "ndjson"]
    mime_types = ["application/json"]
    binary = False

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        text = data.decode("utf-8", errors="replace")
        doc = self._new_doc(source, "json")
        doc.text = text
        try:
            obj = json.loads(text)
            doc.title = _guess_title(obj) or source
            doc.metadata["parsed"] = True
            doc.metadata["top_keys"] = list(obj.keys()) if isinstance(obj, dict) else []
        except json.JSONDecodeError:
            doc.title = source
            doc.metadata["parsed"] = False
        return doc


def _guess_title(obj):
    if isinstance(obj, dict):
        for k in ("title", "name", "标题", "subject"):
            if k in obj and isinstance(obj[k], str):
                return obj[k]
    return None


__all__ = ["JsonParser"]

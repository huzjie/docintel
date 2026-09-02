# -*- coding: utf-8 -*-
"""JSON 渲染。"""
from __future__ import annotations

import json

from ..types import Document


class JsonRenderer:
    def render(self, doc: Document) -> str:
        obj = {
            "title": doc.title,
            "source": doc.source,
            "format": doc.format,
            "metadata": doc.metadata,
            "text": doc.text,
            "blocks": [
                {"type": b.type, "text": b.text, "page": b.page, "level": b.level}
                for b in doc.blocks
            ],
            "tables": [{"caption": t.caption, "rows": t.to_rows()} for t in doc.tables],
            "chunks": [{"id": c.id, "text": c.text} for c in doc.chunks],
            "fields": [{"name": f.name, "value": f.value, "confidence": f.confidence}
                       for f in doc.fields],
        }
        return json.dumps(obj, ensure_ascii=False, indent=2)


__all__ = ["JsonRenderer"]

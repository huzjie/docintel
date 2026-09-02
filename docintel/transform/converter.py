# -*- coding: utf-8 -*-
"""文档格式转换器。"""
from __future__ import annotations

from ..output.renderer import render
from ..types import Document


class Converter:
    """在输出格式间做统一转换。"""

    def __init__(self):
        self._formats = ["markdown", "json", "html", "csv", "txt"]

    def supported(self):
        return self._formats

    def convert(self, doc: Document, target: str) -> str:
        target = target.lower().lstrip(".")
        if target == "txt":
            return doc.text
        return render(doc, target)


__all__ = ["Converter"]

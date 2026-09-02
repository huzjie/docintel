# -*- coding: utf-8 -*-
"""表格抽取统一入口。"""
from __future__ import annotations

from typing import List

from ..types import Document, Table
from .grid import GridTableExtractor
from .heuristic import HeuristicTableExtractor


class TableExtractor:
    """组合网格 + 启发式两种抽取器。"""

    def __init__(self):
        self.grid = GridTableExtractor()
        self.heuristic = HeuristicTableExtractor()

    def extract(self, doc: Document) -> Document:
        existing = list(doc.tables)
        # 从全文再抽一次网格表（解析器可能已带表）
        found = self.grid.extract(doc.text)
        existing += found
        # 去重（按内容哈希）
        seen = set()
        out: List[Table] = []
        for t in existing:
            key = tuple(tuple(c.text for c in r) for r in t.rows)
            if key and key not in seen:
                seen.add(key)
                out.append(t)
        doc.tables = out
        return doc


__all__ = ["TableExtractor"]

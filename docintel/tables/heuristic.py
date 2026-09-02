# -*- coding: utf-8 -*-
"""无边框表格启发式抽取（按列对齐的空白分隔推断）。"""
from __future__ import annotations

from ..types import Table, TableCell


class HeuristicTableExtractor:
    """对空白分隔的多列文本行做启发式聚类。"""

    def extract(self, lines: list[str], min_cols: int = 2) -> Table | None:
        rows = [self._tokenize(l) for l in lines if l.strip()]
        rows = [r for r in rows if len(r) >= min_cols]
        if len(rows) < 2:
            return None
        table = Table(id="h0")
        for r in rows:
            table.rows.append([TableCell(text=c) for c in r])
        return table

    def _tokenize(self, line: str):
        import re
        return [c.strip() for c in re.split(r"\s{2,}|\t", line.strip()) if c.strip()]


__all__ = ["HeuristicTableExtractor"]

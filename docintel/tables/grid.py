# -*- coding: utf-8 -*-
"""有边框（网格）表格抽取。"""
from __future__ import annotations

import re

from ..types import Table, TableCell


class GridTableExtractor:
    """从带制表符 / 竖线分隔的文本行抽取网格表格。"""

    def extract(self, text: str) -> list[Table]:
        tables = []
        current = []
        for line in text.splitlines():
            line = line.rstrip()
            if self._looks_like_row(line):
                current.append(line)
            else:
                if len(current) >= 2:
                    t = self._build(current)
                    if t:
                        tables.append(t)
                current = []
        if len(current) >= 2:
            t = self._build(current)
            if t:
                tables.append(t)
        return tables

    def _looks_like_row(self, line: str) -> bool:
        if "\t" in line:
            return True
        if line.count("|") >= 1:
            return True
        if re.search(r"\s{3,}", line) and "  " in line:
            return True
        return False

    def _build(self, lines) -> Table | None:
        rows = []
        for line in lines:
            cells = self._split_cells(line)
            if cells:
                rows.append([TableCell(text=c) for c in cells])
        if not rows:
            return None
        # 过滤纯分隔行（如 |---|---|）
        rows = [r for r in rows if not all(re.match(r"^[-:]+$", c.text.strip()) for c in r)]
        if len(rows) < 2:
            return None
        return Table(id="g" + str(len(rows)), rows=rows)

    def _split_cells(self, line: str):
        if "\t" in line:
            return [c.strip() for c in line.split("\t")]
        if line.count("|") >= 1:
            parts = line.strip().strip("|").split("|")
            return [c.strip() for c in parts]
        return [c for c in re.split(r"\s{3,}", line.strip()) if c]


__all__ = ["GridTableExtractor"]

# -*- coding: utf-8 -*-
"""CSV 渲染（表格导出）。"""
from __future__ import annotations

import csv
import io

from ..types import Document


class CsvRenderer:
    def render(self, doc: Document) -> str:
        buf = io.StringIO()
        w = csv.writer(buf)
        for t in doc.tables:
            if t.caption:
                w.writerow([t.caption])
            for r in t.to_rows():
                w.writerow(r)
            w.writerow([])
        return buf.getvalue()


__all__ = ["CsvRenderer"]

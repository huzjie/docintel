# -*- coding: utf-8 -*-
"""CSV 解析器（stdlib csv）。"""
from __future__ import annotations

import csv
import io

from ..types import Document, Table, TableCell
from .base import BaseParser


class CsvParser(BaseParser):
    extensions = ["csv", "tsv"]
    mime_types = ["text/csv"]
    binary = False

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        text = data.decode("utf-8", errors="replace")
        delimiter = "\t" if source.lower().endswith(".tsv") else ","
        reader = csv.reader(io.StringIO(text), delimiter=delimiter)
        rows = [row for row in reader]
        doc = self._new_doc(source, "csv")
        doc.text = text
        doc.title = rows[0][0] if rows and rows[0] else source
        table = Table(id="t0", header_rows=1 if rows else 0)
        for r in rows:
            table.rows.append([TableCell(text=c) for c in r])
        doc.tables = [table] if rows else []
        return doc


__all__ = ["CsvParser"]

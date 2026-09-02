# -*- coding: utf-8 -*-
"""XML 解析器（stdlib ElementTree）。"""
from __future__ import annotations

import xml.etree.ElementTree as ET

from ..types import Block, Document, Table, TableCell
from .base import BaseParser


class XmlParser(BaseParser):
    extensions = ["xml"]
    mime_types = ["application/xml", "text/xml"]
    binary = False

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        text = data.decode("utf-8", errors="replace")
        doc = self._new_doc(source, "xml")
        doc.text = text
        try:
            root = ET.fromstring(text)
        except ET.ParseError:
            root = None
        if root is not None:
            doc.title = root.tag
            # 提取叶子文本
            for elem in root.iter():
                if elem.text and elem.text.strip() and not list(elem):
                    pass
            doc.blocks = _walk(root)
            doc.tables = _tables(root)
        return doc


def _walk(elem, blocks=None, depth=0):
    if blocks is None:
        blocks = []
    if elem.text and elem.text.strip():
        blocks.append(Block(id=f"b{len(blocks)}", type="paragraph",
                            text=elem.text.strip(), level=depth))
    for child in elem:
        _walk(child, blocks, depth + 1)
    return blocks


def _tables(root):
    """把同名重复子元素转成表格。"""
    from collections import defaultdict
    groups = defaultdict(list)
    for child in root:
        groups[child.tag].append(child)
    tables = []
    for tag, elems in groups.items():
        if len(elems) < 2:
            continue
        # 子元素字段名集合
        cols = []
        for e in elems:
            for c in e:
                if c.tag not in cols:
                    cols.append(c.tag)
        rows = [cols]
        for e in elems:
            rows.append([(e.findtext(c) or "") for c in cols])
        tables.append(Table(id=f"t{len(tables)}", rows=[[TableCell(text=x) for x in r] for r in rows]))
    return tables


__all__ = ["XmlParser"]

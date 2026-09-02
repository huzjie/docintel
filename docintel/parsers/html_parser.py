# -*- coding: utf-8 -*-
"""HTML 解析器（stdlib HTMLParser）。"""
from __future__ import annotations

import re
from html.parser import HTMLParser

from ..types import Block, Document, Table, TableCell
from .base import BaseParser

_TAG_RE = re.compile(r"<[^>]+>")


class _HtmlToText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip = 0
        self._blocks = []
        self._buf = []
        self._heading = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in ("script", "style"):
            self._skip += 1
        if tag in ("p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr"):
            self._flush()
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            self._heading = int(tag[1])
        if tag == "td":
            self._buf.append("\t")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        if tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
        self._heading = 0

    def _flush(self):
        text = "".join(self._buf).strip()
        self._buf = []
        if text:
            btype = "heading" if self._heading else "paragraph"
            self._blocks.append(Block(id=f"b{len(self._blocks)}", type=btype,
                                      text=text, level=self._heading or 0))

    def handle_data(self, data):
        if self._skip:
            return
        self._buf.append(data)


class HtmlParser(BaseParser):
    extensions = ["html", "htm", "xhtml"]
    mime_types = ["text/html"]
    binary = False

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        text = data.decode("utf-8", errors="replace")
        hp = _HtmlToText()
        hp.feed(text)
        hp.close()
        plain = _TAG_RE.sub(" ", text)
        plain = re.sub(r"\s+", " ", plain).strip()
        doc = self._new_doc(source, "html")
        doc.text = plain
        title_m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
        doc.title = title_m.group(1).strip() if title_m else source
        doc.blocks = hp._blocks
        # 提取简单表格
        doc.tables = _extract_tables(text)
        return doc


def _extract_tables(html: str):
    tables = []
    for m in re.finditer(r"<table[^>]*>(.*?)</table>", html, re.I | re.S):
        body = m.group(1)
        rows = []
        for rm in re.finditer(r"<tr[^>]*>(.*?)</tr>", body, re.I | re.S):
            cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", rm.group(1), re.I | re.S)
            rows.append([TableCell(text=_TAG_RE.sub("", c).strip()) for c in cells])
        if rows:
            tables.append(Table(id=f"t{len(tables)}", rows=rows))
    return tables


__all__ = ["HtmlParser"]

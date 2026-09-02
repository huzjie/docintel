# -*- coding: utf-8 -*-
"""纯文本 / Markdown 解析器。"""
from __future__ import annotations

import re

from ..types import Block, Document
from .base import BaseParser

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_LIST_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
_CN_HEADING = re.compile(r"^[第][一二三四五六七八九十百]+[章节部分条款]+")
_CN_HEADING2 = re.compile(r"^[一二三四五六七八九十]+[、.]")


class TextParser(BaseParser):
    extensions = ["txt", "md", "markdown", "text", "log"]
    mime_types = ["text/plain", "text/markdown"]
    binary = False

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("gbk", errors="replace")
        doc = self._new_doc(source, "text")
        doc.text = text
        doc.title = _first_heading(text) or _first_line(text)
        lines = text.splitlines()
        blocks: list[Block] = []
        for i, line in enumerate(lines):
            s = line.rstrip()
            if not s.strip():
                continue
            m = _HEADING_RE.match(s)
            if m:
                blocks.append(Block(id=f"b{i}", type="heading", text=m.group(2).strip(),
                                   level=len(m.group(1))))
                continue
            if _CN_HEADING.match(s):
                blocks.append(Block(id=f"b{i}", type="heading", text=s.strip(), level=1))
                continue
            if _CN_HEADING2.match(s):
                blocks.append(Block(id=f"b{i}", type="heading", text=s.strip(), level=2))
                continue
            m = _LIST_RE.match(s)
            if m:
                blocks.append(Block(id=f"b{i}", type="list_item", text=m.group(1).strip()))
                continue
            blocks.append(Block(id=f"b{i}", type="paragraph", text=s.strip()))
        doc.blocks = blocks
        return doc


def _first_heading(text: str):
    for line in text.splitlines():
        s = line.strip()
        m = _HEADING_RE.match(s)
        if m:
            return m.group(2).strip()
        if _CN_HEADING.match(s) or _CN_HEADING2.match(s):
            return s
    return None


def _first_line(text: str):
    for line in text.splitlines():
        if line.strip():
            return line.strip()[:120]
    return ""


__all__ = ["TextParser"]

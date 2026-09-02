# -*- coding: utf-8 -*-
"""分块策略。"""
from __future__ import annotations

import re


class FixedStrategy:
    """固定长度分块（按字符数）。"""

    name = "fixed"

    def split(self, text: str, size: int = 800, overlap: int = 120) -> list[str]:
        if not text:
            return []
        out = []
        start = 0
        n = len(text)
        while start < n:
            end = min(start + size, n)
            out.append(text[start:end])
            if end >= n:
                break
            start = end - overlap
        return out


class SlidingStrategy:
    """滑动窗口分块。"""

    name = "sliding"

    def split(self, text: str, size: int = 800, overlap: int = 120) -> list[str]:
        return FixedStrategy().split(text, size, overlap)


class StructureStrategy:
    """按结构（标题/段落边界）分块。"""

    name = "structure"

    def split(self, text: str, size: int = 800, overlap: int = 0) -> list[str]:
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        out = []
        buf = ""
        for p in paras:
            if buf and len(buf) + len(p) + 2 > size:
                out.append(buf)
                buf = p
            else:
                buf = (buf + "\n\n" + p) if buf else p
        if buf:
            out.append(buf)
        return out


class SemanticStrategy:
    """伪语义分块：优先按句子边界，其次结构，兜底固定。"""

    name = "semantic"

    def split(self, text: str, size: int = 800, overlap: int = 120) -> list[str]:
        sentences = re.split(r"(?<=[。！？!?\n])", text)
        out = []
        buf = ""
        for s in sentences:
            if buf and len(buf) + len(s) > size:
                out.append(buf)
                buf = s
            else:
                buf += s
        if buf:
            out.append(buf)
        return [c for c in out if c.strip()]


__all__ = ["FixedStrategy", "SlidingStrategy", "StructureStrategy", "SemanticStrategy"]

# -*- coding: utf-8 -*-
"""块分类工具。"""
from __future__ import annotations

import re

_HEADING_NUM = re.compile(r"^[0-9]+(\.[0-9]+){0,4}[\s、.)]+")
_CN_HEADING = re.compile(r"^[第][一二三四五六七八九十百]+[章节部分条款]+")
_CN_HEADING2 = re.compile(r"^[一二三四五六七八九十]+[、.]")
_LIST = re.compile(r"^\s*[-*+•·]\s+")
_LIST_NUM = re.compile(r"^\s*\d+[.)、]\s+")


def classify_block(text: str, level_hint: int = 0) -> tuple[str, int]:
    """返回 (type, level)。"""
    s = text.strip()
    if not s:
        return "empty", 0
    if level_hint:
        return "heading", level_hint
    if _CN_HEADING.match(s):
        return "heading", 1
    m = _HEADING_NUM.match(s)
    if m:
        dots = m.group(0).count(".")
        return "heading", min(dots + 1, 6)
    if _CN_HEADING2.match(s):
        return "heading", 2
    if _LIST.match(s) or _LIST_NUM.match(s):
        return "list_item", 0
    return "paragraph", 0


__all__ = ["classify_block"]

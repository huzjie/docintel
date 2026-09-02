# -*- coding: utf-8 -*-
"""版面分析启发式规则。"""
from __future__ import annotations

import re


class LayoutRules:
    """一组可配置的启发式规则，用于推断文本块的角色。

    每条规则是 (name, func) 函数，接收文本，返回 (是否命中, type, level)。
    """

    _HEADING_NUM = re.compile(r"^[0-9]+(\.[0-9]+){0,4}[\s、.)]+")
    _CN_HEADING = re.compile(r"^[第][一二三四五六七八九十百]+[章节部分条款]+")
    _CN_HEADING2 = re.compile(r"^[一二三四五六七八九十]+[、.]")
    _LIST = re.compile(r"^\s*[-*+•·]\s+")
    _LIST_NUM = re.compile(r"^\s*\d+[.)、]\s+")
    _CODE = re.compile(r"^\s*(```|def |class |import |from |const |let |var |function )")

    RULES = []

    @classmethod
    def builtin(cls):
        if cls.RULES:
            return cls.RULES
        cls.RULES = [
            ("cn_heading", lambda t: cls._CN_HEADING.match(t.strip()) and ("heading", 1)),
            ("num_heading", lambda t: cls._NUM_HEADING(t)),
            ("cn_heading2", lambda t: cls._CN_HEADING2.match(t.strip()) and ("heading", 2)),
            ("list", lambda t: (cls._LIST.match(t.strip()) or cls._LIST_NUM.match(t.strip())) and ("list_item", 0)),
            ("code", lambda t: cls._CODE.match(t.strip()) and ("code", 0)),
        ]
        return cls.RULES

    @classmethod
    def _NUM_HEADING(cls, t):
        m = cls._HEADING_NUM.match(t.strip())
        if not m:
            return None
        dots = m.group(0).count(".")
        return ("heading", min(dots + 1, 6))

    @classmethod
    def classify(cls, text: str) -> tuple[str, int]:
        for _, fn in cls.builtin():
            r = fn(text)
            if r:
                return r
        return ("paragraph", 0)


__all__ = ["LayoutRules"]

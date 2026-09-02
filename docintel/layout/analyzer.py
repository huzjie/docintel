# -*- coding: utf-8 -*-
"""版面分析器：对文档块做统一分类、去重、顺序整理。"""
from __future__ import annotations

from typing import List

from ..types import Block, Document
from .rules import LayoutRules


class LayoutAnalyzer:
    """基于启发式规则做块级版面分析。"""

    def __init__(self, rules: object = None):
        self.rules = rules or LayoutRules

    def analyze(self, doc: Document) -> Document:
        # 若解析器已产出 blocks，对其重分类 + 排序；否则从 text 切块
        if not doc.blocks and doc.text:
            doc.blocks = self._blocks_from_text(doc.text)
        doc.blocks = self._normalize(doc.blocks)
        return doc

    def _blocks_from_text(self, text: str) -> List[Block]:
        blocks = []
        for i, para in enumerate(text.split("\n")):
            para = para.strip()
            if not para:
                continue
            btype, level = self.rules.classify(para)
            blocks.append(Block(id=f"b{i}", type=btype, text=para, level=level))
        return blocks

    def _normalize(self, blocks: List[Block]) -> List[Block]:
        out: List[Block] = []
        seen = set()
        for b in blocks:
            if not b.text.strip():
                continue
            key = (b.type, b.text.strip()[:80])
            if key in seen:
                continue
            seen.add(key)
            if b.type == "paragraph":
                b.type, b.level = self.rules.classify(b.text)
            out.append(b)
        return out


__all__ = ["LayoutAnalyzer"]

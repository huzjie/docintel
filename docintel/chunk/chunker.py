# -*- coding: utf-8 -*-
"""分块器：按策略把文档切成 Chunk。"""
from __future__ import annotations

import hashlib

from ..types import Chunk, Document
from .strategies import FixedStrategy, SemanticStrategy, StructureStrategy

_STRATEGIES = {
    "fixed": FixedStrategy(),
    "sliding": FixedStrategy(),
    "structure": StructureStrategy(),
    "semantic": SemanticStrategy(),
}


class Chunker:
    def __init__(self, strategy: str = "semantic", size: int = 800, overlap: int = 120):
        self.strategy = strategy
        self.size = size
        self.overlap = overlap

    def chunk(self, doc: Document) -> Document:
        strat = _STRATEGIES.get(self.strategy, SemanticStrategy())
        parts = strat.split(doc.text, self.size, self.overlap)
        chunks = []
        offset = 0
        for i, part in enumerate(parts):
            cid = "c" + hashlib.sha1(part.encode("utf-8")).hexdigest()[:12]
            chunks.append(Chunk(
                id=cid, text=part, start=offset,
                end=offset + len(part), meta={"strategy": self.strategy},
            ))
            offset += len(part) + 1
        doc.chunks = chunks
        return doc


__all__ = ["Chunker"]

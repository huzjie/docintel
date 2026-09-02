# -*- coding: utf-8 -*-
"""语义分块：把文档切分成适合 RAG 的片段。"""
from .strategies import FixedStrategy, SlidingStrategy, StructureStrategy, SemanticStrategy
from .chunker import Chunker

__all__ = ["FixedStrategy", "SlidingStrategy", "StructureStrategy", "SemanticStrategy", "Chunker"]

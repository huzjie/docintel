# -*- coding: utf-8 -*-
"""docintel 核心数据模型（纯 dataclass，零依赖）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Span:
    """文本区间（字符偏移）。"""
    start: int
    end: int

    @property
    def text(self) -> str:
        return ""


@dataclass
class Block:
    """版面分析产出的文本块。"""
    id: str
    type: str                      # title / heading / paragraph / list_item / table / image / header / footer / code
    text: str = ""
    page: int = 0
    level: int = 0                 # heading 层级 1-6
    confidence: float = 1.0
    bbox: Optional[List[float]] = None   # [x0, y0, x1, y1] 归一化
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    """表格单元格。"""
    text: str = ""
    rowspan: int = 1
    colspan: int = 1
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Table:
    """结构化表格。"""
    id: str
    rows: List[List[TableCell]] = field(default_factory=list)
    page: int = 0
    caption: str = ""
    header_rows: int = 0
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_rows(self) -> List[List[str]]:
        return [[c.text for c in row] for row in self.rows]

    def to_dict(self) -> List[Dict[str, str]]:
        """首行为表头时转成字典列表。"""
        if not self.rows:
            return []
        header = [c.text for c in self.rows[0]]
        out = []
        for row in self.rows[1:]:
            out.append({header[i]: c.text for i, c in enumerate(row) if i < len(header)})
        return out


@dataclass
class ImageRef:
    """文档内图片引用。"""
    id: str
    data: bytes = b""
    mime: str = "image/png"
    page: int = 0
    caption: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Page:
    """文档页。"""
    index: int
    text: str = ""
    blocks: List[Block] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)
    images: List[ImageRef] = field(default_factory=list)


@dataclass
class Chunk:
    """语义分块（供 RAG）。"""
    id: str
    text: str
    page: int = 0
    start: int = 0
    end: int = 0
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedField:
    """LLM 抽取出的结构化字段。"""
    name: str
    value: Any
    confidence: float = 1.0
    source: str = ""


@dataclass
class Document:
    """解析后的完整文档。"""
    source: str = ""               # 源文件路径或 URL
    format: str = ""               # pdf/docx/xlsx/...
    title: str = ""
    text: str = ""
    pages: List[Page] = field(default_factory=list)
    blocks: List[Block] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)
    images: List[ImageRef] = field(default_factory=list)
    chunks: List[Chunk] = field(default_factory=list)
    fields: List[ExtractedField] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    def summary(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "format": self.format,
            "title": self.title,
            "pages": len(self.pages),
            "blocks": len(self.blocks),
            "tables": len(self.tables),
            "images": len(self.images),
            "chunks": len(self.chunks),
            "fields": len(self.fields),
            "word_count": self.word_count,
        }


@dataclass
class ParseResult:
    """一次解析任务的结果封装。"""
    document: Document
    elapsed_ms: int = 0
    warnings: List[str] = field(default_factory=list)
    pipeline_log: List[str] = field(default_factory=list)


__all__ = [
    "Span", "Block", "TableCell", "Table", "ImageRef", "Page",
    "Chunk", "ExtractedField", "Document", "ParseResult",
]

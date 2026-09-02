# -*- coding: utf-8 -*-
"""解析管道编排：解析 -> 版面 -> 表格 -> OCR -> 分块 -> 抽取 -> 输出。"""
from __future__ import annotations

import time
from typing import Dict, List, Optional

from ..chunk.chunker import Chunker
from ..extract.llm_extractor import LlmExtractor
from ..extract.schema import ExtractionSchema
from ..layout.analyzer import LayoutAnalyzer
from ..ocr.engine import get_ocr_engine
from ..observability.metrics import Metrics
from ..output.renderer import render
from ..providers.base import get_provider
from ..security.redact import PiiRedactor
from ..tables.extractor import TableExtractor
from ..types import Document, ParseResult
from .loader import load_bytes


class Pipeline:
    """可配置的文档解析管道。"""

    def __init__(self, config: Dict):
        self.config = config
        self.metrics = Metrics()
        self.ocr = get_ocr_engine(config)
        self.layout = LayoutAnalyzer()
        self.tables = TableExtractor()
        self.redactor = PiiRedactor(config.get("security", {}).get("pii_placeholder", "[REDACTED]"))

    def run(self, data: bytes, source: str = "", ext: str = "") -> ParseResult:
        start = time.time()
        log: List[str] = []
        warnings: List[str] = []
        pipe = self.config.get("pipeline", {})

        doc = load_bytes(data, source=source, ext=ext)
        log.append("parse: ok")

        if pipe.get("enable_layout", True):
            doc = self.layout.analyze(doc)
            log.append(f"layout: {len(doc.blocks)} blocks")

        if pipe.get("enable_table", True):
            doc = self.tables.extract(doc)
            log.append(f"table: {len(doc.tables)} tables")

        # 图片文档 / 含图 PDF 走 OCR
        if pipe.get("enable_ocr", True) and not doc.text.strip() and doc.images:
            for img in doc.images:
                text = self.ocr.recognize(img.data)
                if text:
                    doc.text += text
            log.append(f"ocr: {'ok' if doc.text.strip() else 'empty'}")

        # PII 脱敏
        if self.config.get("security", {}).get("enable_pii_redact", True):
            doc.text, n = self.redactor.redact(doc.text)
            if n:
                log.append(f"redact: {n} 处 PII 已脱敏")

        if pipe.get("enable_chunk", True):
            chunker = Chunker(
                strategy=pipe.get("chunk_strategy", "semantic"),
                size=pipe.get("chunk_size", 800),
                overlap=pipe.get("chunk_overlap", 120),
            )
            doc = chunker.chunk(doc)
            log.append(f"chunk: {len(doc.chunks)} chunks")

        if pipe.get("enable_extract", False):
            schema_name = pipe.get("extract_schema", "generic")
            schema = _resolve_schema(schema_name)
            provider = get_provider(self.config)
            extractor = LlmExtractor(
                provider, schema=schema,
                max_tokens=self.config.get("extract", {}).get("max_tokens", 2048),
            )
            doc = extractor.extract(doc)
            log.append(f"extract: {len(doc.fields)} fields")

        elapsed = int((time.time() - start) * 1000)
        self.metrics.inc("documents_parsed")
        self.metrics.observe("parse_latency_ms", elapsed)
        return ParseResult(document=doc, elapsed_ms=elapsed, warnings=warnings, pipeline_log=log)

    def run_file(self, path: str) -> ParseResult:
        from pathlib import Path
        p = Path(path)
        return self.run(p.read_bytes(), source=str(p), ext=p.suffix)

    def to_output(self, result: ParseResult, fmt: str = "markdown") -> str:
        return render(result.document, fmt)


def _resolve_schema(name: str) -> ExtractionSchema:
    mapping = {
        "invoice": ExtractionSchema.invoice,
        "contract": ExtractionSchema.contract,
        "resume": ExtractionSchema.resume,
    }
    fn = mapping.get(name)
    if fn:
        return fn()
    return ExtractionSchema(name="generic")


__all__ = ["Pipeline"]

# -*- coding: utf-8 -*-
"""解析器注册表与路由。"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from ..errors import UnsupportedFormatError
from ..types import Document
from .base import BaseParser


class ParserRegistry:
    """按扩展名 / MIME 路由到具体解析器。"""

    def __init__(self) -> None:
        self._parsers: Dict[str, BaseParser] = {}

    def register(self, parser: BaseParser) -> None:
        for ext in parser.extensions:
            self._parsers[ext.lower().lstrip(".")] = parser

    def get(self, ext: str) -> Optional[BaseParser]:
        return self._parsers.get(ext.lower().lstrip("."))

    def supported_extensions(self) -> List[str]:
        return sorted(self._parsers.keys())

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        ext = ext.lower().lstrip(".")
        if not ext:
            ext = Path(source).suffix.lower().lstrip(".") if source else ""
        parser = self.get(ext)
        if parser is None:
            raise UnsupportedFormatError(f"不支持的格式: {ext or source}")
        return parser.parse(data, source=source, ext=ext)


_registry: Optional[ParserRegistry] = None


def _build_registry() -> ParserRegistry:
    from .text_parser import TextParser
    from .html_parser import HtmlParser
    from .json_parser import JsonParser
    from .pdf_parser import PdfParser
    from .docx_parser import DocxParser
    from .xlsx_parser import XlsxParser
    from .pptx_parser import PptxParser
    from .csv_parser import CsvParser
    from .image_parser import ImageParser
    from .email_parser import EmailParser
    from .xml_parser import XmlParser

    reg = ParserRegistry()
    for p in (TextParser(), HtmlParser(), JsonParser(), PdfParser(),
              DocxParser(), XlsxParser(), PptxParser(), CsvParser(),
              ImageParser(), EmailParser(), XmlParser()):
        reg.register(p)
    return reg


def get_registry() -> ParserRegistry:
    global _registry
    if _registry is None:
        _registry = _build_registry()
    return _registry


def get_parser(ext: str) -> Optional[BaseParser]:
    return get_registry().get(ext)


def list_parsers() -> List[str]:
    return get_registry().supported_extensions()


def parse_file(path: str) -> Document:
    p = Path(path)
    data = p.read_bytes()
    return get_registry().parse(data, source=str(p), ext=p.suffix)


__all__ = ["ParserRegistry", "get_registry", "get_parser", "list_parsers", "parse_file"]

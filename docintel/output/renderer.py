# -*- coding: utf-8 -*-
"""输出渲染统一入口。"""
from __future__ import annotations

from ..errors import ConfigError
from ..types import Document
from .csv_output import CsvRenderer
from .html_output import HtmlRenderer
from .json_output import JsonRenderer
from .markdown import MarkdownRenderer


def render(doc: Document, fmt: str) -> str:
    fmt = fmt.lower().lstrip(".")
    if fmt in ("md", "markdown"):
        return MarkdownRenderer().render(doc)
    if fmt == "json":
        return JsonRenderer().render(doc)
    if fmt in ("html", "htm"):
        return HtmlRenderer().render(doc)
    if fmt == "csv":
        return CsvRenderer().render(doc)
    raise ConfigError(f"不支持的输出格式: {fmt}")


__all__ = ["render"]

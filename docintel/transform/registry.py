# -*- coding: utf-8 -*-
"""格式转换统一入口。"""
from __future__ import annotations

from ..types import Document
from .converter import Converter

_converter = Converter()


def convert(doc: Document, target: str) -> str:
    return _converter.convert(doc, target)


def supported_formats():
    return _converter.supported()


__all__ = ["convert", "supported_formats"]

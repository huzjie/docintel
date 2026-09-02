# -*- coding: utf-8 -*-
"""解析器基类。"""
from __future__ import annotations

from typing import List, Optional

from ..types import Document, ImageRef, Table


class BaseParser:
    """所有解析器的抽象基类。

    子类实现 `parse_bytes(data, source)`，返回初步的 Document。
    """

    #: 支持的扩展名列表（小写，不含点）
    extensions: List[str] = []
    #: 支持检查的 MIME 类型（可选）
    mime_types: List[str] = []
    #: 是否二进制格式
    binary: bool = False

    @classmethod
    def can_handle(cls, ext: str) -> bool:
        return ext.lower().lstrip(".") in cls.extensions

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        raise NotImplementedError

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        raise NotImplementedError

    def _new_doc(self, source: str, fmt: str) -> Document:
        from ..types import Document
        return Document(source=source, format=fmt)


__all__ = ["BaseParser"]

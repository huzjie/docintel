# -*- coding: utf-8 -*-
"""文件加载入口：读字节 + 路由解析器。"""
from __future__ import annotations

from pathlib import Path

from ..parsers.registry import get_registry
from ..security.policy import SecurityPolicy, enforce_file_limits
from ..types import Document


def load_bytes(data: bytes, source: str = "", ext: str = "",
               policy: SecurityPolicy = None) -> Document:
    policy = policy or SecurityPolicy()
    enforce_file_limits(data, policy)
    return get_registry().parse(data, source=source, ext=ext)


def load_file(path: str, policy: SecurityPolicy = None) -> Document:
    p = Path(path)
    data = p.read_bytes()
    return load_bytes(data, source=str(p), ext=p.suffix, policy=policy)


__all__ = ["load_bytes", "load_file"]

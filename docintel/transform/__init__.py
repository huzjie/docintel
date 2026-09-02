# -*- coding: utf-8 -*-
"""格式转换：文档 -> Markdown/HTML/JSON/CSV/TXT。"""
from .converter import Converter
from .registry import convert

__all__ = ["Converter", "convert"]

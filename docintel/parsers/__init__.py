# -*- coding: utf-8 -*-
"""文档解析器集合。"""
from .base import BaseParser
from .registry import ParserRegistry, get_parser, list_parsers, parse_file

__all__ = ["BaseParser", "ParserRegistry", "get_parser", "list_parsers", "parse_file"]

# -*- coding: utf-8 -*-
"""docintel — 智能文档解析与结构化抽取平台。

把 PDF / Word / Excel / PPT / HTML / 图片 / 邮件等非结构化文档，
一键转成 AI-ready 的结构化数据（Markdown / JSON / 表格 / 语义字段），
供 RAG、知识库、LLM 应用直接消费。

对标 Cohere Parse 5：复杂文档、表格、图片 → 干净、可检索的结构化数据。
"""
from .version import __version__

__all__ = ["__version__"]

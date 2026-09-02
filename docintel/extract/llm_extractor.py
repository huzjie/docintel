# -*- coding: utf-8 -*-
"""LLM 结构化抽取器：调用 Provider 抽取字段，容错 JSON 解析。"""
from __future__ import annotations

import json
import re
from typing import List

from ..errors import ExtractError
from ..providers.base import BaseProvider
from ..types import Document, ExtractedField
from .prompts import build_extraction_prompt
from .schema import ExtractionSchema


class LlmExtractor:
    def __init__(self, provider: BaseProvider, schema: ExtractionSchema = None,
                 max_tokens: int = 2048, temperature: float = 0.0, retries: int = 2):
        self.provider = provider
        self.schema = schema or ExtractionSchema(name="generic")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.retries = retries

    def extract(self, doc: Document) -> Document:
        prompt = build_extraction_prompt(self.schema, doc.text)
        obj = None
        last_err = None
        for _ in range(self.retries + 1):
            try:
                raw = self.provider.complete(prompt, max_tokens=self.max_tokens,
                                             temperature=self.temperature)
                obj = _parse_json(raw)
                break
            except Exception as e:
                last_err = e
        if obj is None:
            raise ExtractError(f"LLM 抽取失败: {last_err}")
        for f in self.schema.fields:
            val = obj.get(f.name)
            if val is None:
                continue
            doc.fields.append(ExtractedField(name=f.name, value=val))
        return doc


def _parse_json(raw: str) -> dict:
    text = raw.strip()
    # 剥离 markdown 代码块
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    # 取第一个 { ... } 平衡块
    start = text.find("{")
    if start == -1:
        raise ExtractError("输出中未找到 JSON 对象")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                text = text[start:i + 1]
                break
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ExtractError("抽取结果不是对象")
    return obj


__all__ = ["LlmExtractor"]

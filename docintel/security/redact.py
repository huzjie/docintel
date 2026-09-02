# -*- coding: utf-8 -*-
"""PII 脱敏（正则，零依赖）。"""
from __future__ import annotations

import re

_PATTERNS = [
    (re.compile(r"\b1[3-9]\d{9}\b"), "手机号"),
    (re.compile(r"\b\d{15}(\d{2}[0-9Xx])?\b"), "身份证"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "邮箱"),
    (re.compile(r"\b(?:4\d{3}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4})\b"), "银行卡"),
]


class PiiRedactor:
    def __init__(self, placeholder: str = "[REDACTED]"):
        self.placeholder = placeholder

    def redact(self, text: str) -> tuple[str, int]:
        n = 0
        for pat, _name in _PATTERNS:
            text, c = pat.subn(self.placeholder, text)
            n += c
        return text, n


__all__ = ["PiiRedactor"]

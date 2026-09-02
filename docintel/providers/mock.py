# -*- coding: utf-8 -*-
"""确定性 Mock Provider：离线端到端可跑。"""
from __future__ import annotations

import hashlib
import json

from .base import BaseProvider


class MockProvider(BaseProvider):
    """无网络、确定性输出，供离线冒烟与测试。

    对抽取提示词返回一份「看似合理」的 JSON，键从字段定义里解析，
    值用文本哈希生成，保证同一输入同一输出。
    """

    name = "mock"

    def complete(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.0) -> str:
        # 解析字段名：- 字段名（类型）
        import re
        fields = re.findall(r"-\s*([^（\n]+)（(\w+)）", prompt)
        obj = {}
        for name, typ in fields:
            obj[name] = _mock_value(name, typ, prompt)
        return json.dumps(obj, ensure_ascii=False)


def _mock_value(name: str, typ: str, prompt: str) -> object:
    h = int(hashlib.sha1((name + prompt[:500]).encode("utf-8")).hexdigest(), 16)
    if typ == "int":
        return h % 1000
    if typ == "float":
        return round((h % 100000) / 100.0, 2)
    if typ == "bool":
        return bool(h % 2)
    if typ == "list":
        return ["技能A", "技能B", "技能C"]
    if typ == "date":
        return f"2026-{(h % 12) + 1:02d}-{(h % 28) + 1:02d}"
    return f"mock_{name}_{h % 10000}"


__all__ = ["MockProvider"]

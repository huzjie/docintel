# -*- coding: utf-8 -*-
"""抽取提示词模板。"""
from __future__ import annotations

from .schema import ExtractionSchema


def build_extraction_prompt(schema: ExtractionSchema, text: str, max_len: int = 12000) -> str:
    fields_desc = "\n".join(
        f"- {f.name}（{f.type}）：{f.description}" + ("【必填】" if f.required else "")
        for f in schema.fields
    )
    snippet = text[:max_len]
    return f"""你是结构化信息抽取引擎。请从以下文档中抽取字段，只输出合法 JSON。

抽取任务：{schema.name} - {schema.description}
字段定义：
{fields_desc}

要求：
1. 只输出一个 JSON 对象，键为字段名，值为抽取结果（找不到填 null）。
2. list 类型字段输出字符串数组。
3. date 类型统一为 YYYY-MM-DD。
4. 不要输出任何 JSON 以外的内容、解释或代码块标记。

文档内容（开始）：
{snippet}
文档内容（结束）

JSON 输出：
"""


__all__ = ["build_extraction_prompt"]

# -*- coding: utf-8 -*-
"""Markdown 渲染。"""
from __future__ import annotations

from ..types import Document


class MarkdownRenderer:
    def render(self, doc: Document) -> str:
        lines = []
        if doc.title:
            lines.append(f"# {doc.title}")
            lines.append("")
        for b in doc.blocks:
            if b.type == "heading":
                lines.append(f"{'#' * max(1, min(6, b.level or 1))} {b.text}")
            elif b.type == "list_item":
                lines.append(f"- {b.text}")
            elif b.type == "code":
                lines.append(f"```\n{b.text}\n```")
            else:
                lines.append(b.text)
            lines.append("")
        for i, t in enumerate(doc.tables):
            if t.caption:
                lines.append(f"**表 {i + 1} {t.caption}**")
            rows = t.to_rows()
            if rows:
                lines.append("| " + " | ".join(rows[0]) + " |")
                lines.append("|" + "---|" * len(rows[0]))
                for r in rows[1:]:
                    lines.append("| " + " | ".join(r) + " |")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


__all__ = ["MarkdownRenderer"]

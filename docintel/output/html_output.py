# -*- coding: utf-8 -*-
"""HTML 渲染。"""
from __future__ import annotations

import html

from ..types import Document


class HtmlRenderer:
    def render(self, doc: Document) -> str:
        parts = ["<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>",
                 html.escape(doc.title or "docintel"), "</title>",
                 "<style>body{font-family:sans-serif;max-width:900px;margin:2em auto;padding:0 1em}",
                 "table{border-collapse:collapse;width:100%;margin:1em 0}td,th{border:1px solid #ddd;padding:6px 10px}",
                 "h1,h2,h3{color:#333}</style></head><body>"]
        if doc.title:
            parts.append(f"<h1>{html.escape(doc.title)}</h1>")
        for b in doc.blocks:
            if b.type == "heading":
                lvl = max(1, min(6, b.level or 1))
                parts.append(f"<h{lvl}>{html.escape(b.text)}</h{lvl}>")
            elif b.type == "list_item":
                parts.append(f"<li>{html.escape(b.text)}</li>")
            elif b.type == "code":
                parts.append(f"<pre><code>{html.escape(b.text)}</code></pre>")
            else:
                parts.append(f"<p>{html.escape(b.text)}</p>")
        for t in doc.tables:
            parts.append("<table>")
            for r in t.to_rows():
                parts.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>")
            parts.append("</table>")
        parts.append("</body></html>")
        return "".join(parts)


__all__ = ["HtmlRenderer"]

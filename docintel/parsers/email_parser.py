# -*- coding: utf-8 -*-
"""邮件（.eml / RFC 822）解析器（stdlib email）。"""
from __future__ import annotations

import email
from email import policy
from email.parser import BytesParser

from ..types import Block, Document
from .base import BaseParser


class EmailParser(BaseParser):
    extensions = ["eml", "emlx", "mht"]
    mime_types = ["message/rfc822"]
    binary = True

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        doc = self._new_doc(source, "email")
        msg = BytesParser(policy=policy.default).parsebytes(data)
        doc.title = msg.get("Subject", source)
        doc.metadata["from"] = msg.get("From", "")
        doc.metadata["to"] = msg.get("To", "")
        doc.metadata["date"] = msg.get("Date", "")
        # 提取正文
        parts = []
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    parts.append(part.get_content())
                except Exception:
                    parts.append(part.get_payload(decode=True).decode("utf-8", "replace") if part.get_payload(decode=True) else "")
        body = "\n".join(parts)
        doc.text = body
        blocks = []
        blocks.append(Block(id="b0", type="heading", text=f"主题：{doc.title}", level=1))
        for i, line in enumerate(body.splitlines()):
            if line.strip():
                blocks.append(Block(id=f"b{i + 1}", type="paragraph", text=line.strip()))
        doc.blocks = blocks
        return doc


__all__ = ["EmailParser"]

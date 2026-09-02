# -*- coding: utf-8 -*-
"""PDF 解析器。

优先尝试惰性导入 pypdf；未安装时用 stdlib 做粗粒度文本抽取
（按 stream 中 (Tj/TJ) 文本指令提取，仅能覆盖无压缩文本 PDF），
保证离线零依赖也能基本可用。
"""
from __future__ import annotations

import re
import zlib

from ..types import Block, Document, Page
from .base import BaseParser


class PdfParser(BaseParser):
    extensions = ["pdf"]
    mime_types = ["application/pdf"]
    binary = True

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        doc = self._new_doc(source, "pdf")
        pages_text, title = self._try_pypdf(data) or self._stdlib_extract(data)
        doc.title = title or source
        doc.pages = [Page(index=i, text=t) for i, t in enumerate(pages_text)]
        doc.text = "\n".join(pages_text)
        for i, t in enumerate(pages_text):
            for j, para in enumerate(_split_paragraphs(t)):
                doc.blocks.append(Block(id=f"p{i}b{j}", type="paragraph",
                                        text=para, page=i + 1))
        return doc

    def _try_pypdf(self, data: bytes):
        try:
            from io import BytesIO
            from pypdf import PdfReader
        except Exception:
            return None
        try:
            reader = PdfReader(BytesIO(data))
            texts = []
            for page in reader.pages:
                texts.append(page.extract_text() or "")
            meta = reader.metadata
            title = None
            if meta and meta.title:
                title = str(meta.title)
            return texts, title
        except Exception:
            return None

    def _stdlib_extract(self, data: bytes):
        texts: list[str] = []
        # 处理 FlateDecode 流
        streams = []
        for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
            raw = m.group(1)
            try:
                raw = raw.strip(b"\r\n")
                streams.append(zlib.decompress(raw))
            except Exception:
                streams.append(raw)
        # 从解压流里抽 Tj/TJ 文本
        found = []
        for s in streams:
            found += re.findall(rb"\(([^)]*)\)\s*Tj", s)
            found += re.findall(rb"\[([^\]]*)\]\s*TJ", s)
        if found:
            texts = []
            for f in found:
                txt = f.decode("latin-1", errors="replace")
                txt = re.sub(r"\\([()])", r"\1", txt)
                texts.append(txt)
        if not texts:
            # 兜底：直接搜文本对象里的字符串
            texts = ["（PDF 内容需 pypdf 以完整解析；已用 stdlib 粗提取，可能不完整）"]
        title = None
        tm = re.search(rb"/Title\s*\(([^)]*)\)", data)
        if tm:
            title = tm.group(1).decode("latin-1", errors="replace")
        return texts, title


def _split_paragraphs(text: str):
    for part in re.split(r"\n\s*\n", text):
        part = part.strip()
        if part:
            yield part


__all__ = ["PdfParser"]

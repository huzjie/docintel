# -*- coding: utf-8 -*-
"""PPTX 解析器（zip + XML，纯 stdlib）。"""
from __future__ import annotations

import io
import re
import zipfile
import xml.etree.ElementTree as ET

from ..types import Block, Document, Page
from .base import BaseParser

_A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


class PptxParser(BaseParser):
    extensions = ["pptx", "ppt"]
    mime_types = ["application/vnd.openxmlformats-officedocument.presentationml.presentation"]
    binary = True

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        doc = self._new_doc(source, "pptx")
        try:
            zf = zipfile.ZipFile(io.BytesIO(data))
        except zipfile.BadZipFile:
            doc.text = "（.ppt 老格式需转换，仅支持 .pptx）"
            doc.title = source
            return doc
        slides = sorted(
            [n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml", n)],
            key=lambda n: int(re.search(r"slide(\d+)", n).group(1)),
        )
        pages = []
        for sn in slides:
            root = ET.fromstring(zf.read(sn))
            texts = []
            for t in root.iter(f"{{{_A_NS}}}t"):
                if t.text:
                    texts.append(t.text)
            pages.append(Page(index=len(pages), text="\n".join(texts)))
        doc.pages = pages
        doc.text = "\n".join(p.text for p in pages)
        doc.title = pages[0].text.split("\n")[0] if pages and pages[0].text else source
        for p in pages:
            for j, line in enumerate(p.text.split("\n")):
                if line.strip():
                    doc.blocks.append(Block(id=f"p{p.index}b{j}", type="paragraph",
                                            text=line.strip(), page=p.index + 1))
        return doc


__all__ = ["PptxParser"]

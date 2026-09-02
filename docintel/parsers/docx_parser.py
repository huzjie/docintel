# -*- coding: utf-8 -*-
"""DOCX 解析器（zip + XML，纯 stdlib）。"""
from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET

from ..types import Block, Document, Table, TableCell
from .base import BaseParser

_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}


def _q(tag: str) -> str:
    return "{%s}%s" % (_NS["w"], tag)


class DocxParser(BaseParser):
    extensions = ["docx", "doc"]
    mime_types = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    binary = True

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        doc = self._new_doc(source, "docx")
        try:
            zf = zipfile.ZipFile(_bytes_to_file(data))
        except (zipfile.BadZipFile, OSError):
            # .doc 老格式无法用 zip 解，给提示
            doc.text = "（.doc 老格式需 LibreOffice/antiword 转换，仅支持 .docx）"
            doc.title = source
            return doc
        try:
            root = ET.fromstring(zf.read("word/document.xml"))
        except KeyError:
            root = None

        paragraphs = []
        if root is not None:
            body = root.find(_q("body"))
            if body is not None:
                for para in body.iter(_q("p")):
                    texts = []
                    for t in para.iter(_q("t")):
                        texts.append(t.text or "")
                    line = "".join(texts).strip()
                    if line:
                        paragraphs.append(line)
        text = "\n".join(paragraphs)
        doc.text = text
        doc.title = paragraphs[0] if paragraphs else source

        # 表格
        if root is not None:
            body = root.find(_q("body"))
            for i, tbl in enumerate(body.iter(_q("tbl")) if body is not None else []):
                table = Table(id=f"t{i}")
                for tr in tbl.iter(_q("tr")):
                    cells = []
                    for tc in tr.iter(_q("tc")):
                        cell_text = "".join(t.text or "" for t in tc.iter(_q("t"))).strip()
                        cells.append(TableCell(text=cell_text))
                    if cells:
                        table.rows.append(cells)
                if table.rows:
                    doc.tables.append(table)

        # 粗分块
        for i, para in enumerate(paragraphs):
            btype = "heading" if _is_heading(para) else "paragraph"
            doc.blocks.append(Block(id=f"b{i}", type=btype, text=para))
        return doc


def _is_heading(text: str) -> bool:
    if len(text) > 80:
        return False
    if re.match(r"^[0-9]+(\.[0-9]+)*[\s、.]+", text):
        return True
    if re.match(r"^[第][一二三四五六七八九十]+[章节部分]", text):
        return True
    return False


def _bytes_to_file(data: bytes):
    import io
    return io.BytesIO(data)


__all__ = ["DocxParser"]

# -*- coding: utf-8 -*-
"""图片解析器：识别图片内容，走 OCR + 可选 VLM 描述。"""
from __future__ import annotations

from ..types import Document, ImageRef
from .base import BaseParser


class ImageParser(BaseParser):
    extensions = ["png", "jpg", "jpeg", "bmp", "tiff", "tif", "webp", "gif"]
    mime_types = ["image/png", "image/jpeg", "image/bmp", "image/tiff", "image/webp"]
    binary = True

    def parse(self, data: bytes, source: str = "", ext: str = "") -> Document:
        return self.parse_bytes(data, source)

    def parse_bytes(self, data: bytes, source: str = "") -> Document:
        ext = (source.rsplit(".", 1)[-1] if "." in source else "png").lower()
        mime = _guess_mime(ext)
        doc = self._new_doc(source, "image")
        doc.images = [ImageRef(id="img0", data=data, mime=mime)]
        doc.metadata["width"] = _png_size(data)[0] if ext == "png" else None
        doc.metadata["height"] = _png_size(data)[1] if ext == "png" else None
        doc.title = source
        # OCR 由 pipeline 阶段填充 doc.text
        return doc


def _guess_mime(ext: str) -> str:
    return {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "bmp": "image/bmp", "tiff": "image/tiff", "tif": "image/tiff",
        "webp": "image/webp", "gif": "image/gif",
    }.get(ext, "image/png")


def _png_size(data: bytes):
    """PNG IHDR 里读宽高。"""
    import struct
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


__all__ = ["ImageParser"]

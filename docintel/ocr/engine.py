# -*- coding: utf-8 -*-
"""OCR 引擎抽象与实现。"""
from __future__ import annotations

from typing import List

from ..errors import OcrError


class OcrEngine:
    """OCR 引擎基类。"""

    name = "base"

    def recognize(self, image_bytes: bytes) -> str:
        raise NotImplementedError


class MockOcrEngine(OcrEngine):
    """确定性 mock：图片里通常是空识别（用于离线冒烟）。"""

    name = "mock"

    def recognize(self, image_bytes: bytes) -> str:
        # 无真实 OCR 时返回占位说明，保证管线可跑
        return ""


class TesseractEngine(OcrEngine):
    """惰性 tesseract 引擎（需安装 pytesseract + tesseract 二进制）。"""

    name = "tesseract"

    def __init__(self, tesseract_cmd: str = "tesseract", lang: str = "chi_sim+eng"):
        self.tesseract_cmd = tesseract_cmd
        self.lang = lang

    def recognize(self, image_bytes: bytes) -> str:
        try:
            import pytesseract
            from PIL import Image
            import io
        except ImportError as e:
            raise OcrError("OCR 需安装 pytesseract + Pillow") from e
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
        img = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(img, lang=self.lang)


def get_ocr_engine(config: dict) -> OcrEngine:
    name = (config.get("ocr") or {}).get("engine", "mock")
    if name == "tesseract":
        return TesseractEngine(
            tesseract_cmd=config.get("ocr", {}).get("tesseract_cmd", "tesseract"),
            lang=config.get("ocr", {}).get("lang", "chi_sim+eng"),
        )
    return MockOcrEngine()


__all__ = ["OcrEngine", "MockOcrEngine", "TesseractEngine", "get_ocr_engine"]

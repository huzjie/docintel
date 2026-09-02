# -*- coding: utf-8 -*-
from docintel.transform.registry import convert, supported_formats
from docintel.types import Block, Document


def _doc():
    d = Document(source="x", format="text", title="标题", text="正文内容")
    d.blocks = [Block(id="b0", type="heading", text="标题", level=1)]
    return d


def test_supported():
    assert "markdown" in supported_formats()


def test_convert_txt():
    assert convert(_doc(), "txt") == "正文内容"


def test_convert_markdown():
    assert "# 标题" in convert(_doc(), "markdown")

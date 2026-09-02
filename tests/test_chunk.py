# -*- coding: utf-8 -*-
from docintel.chunk.chunker import Chunker
from docintel.types import Document


def _doc(text):
    d = Document(source="x", format="text", text=text)
    return d


def test_fixed_chunk():
    text = "字" * 2000
    d = Chunker(strategy="fixed", size=500, overlap=50).chunk(_doc(text))
    assert len(d.chunks) >= 4


def test_semantic_chunk():
    text = "第一句。第二句！第三句？" * 50
    d = Chunker(strategy="semantic", size=100, overlap=10).chunk(_doc(text))
    assert len(d.chunks) > 1
    assert all(c.text.strip() for c in d.chunks)

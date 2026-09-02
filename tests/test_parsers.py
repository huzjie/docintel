# -*- coding: utf-8 -*-
from docintel.parsers.registry import get_registry, list_parsers
from docintel.parsers.text_parser import TextParser
from docintel.parsers.csv_parser import CsvParser
from docintel.parsers.html_parser import HtmlParser
from docintel.parsers.json_parser import JsonParser


def test_text_parser():
    p = TextParser()
    doc = p.parse("第一章 背景\n这是正文。\n- 列表项\n".encode("utf-8"))
    assert doc.format == "text"
    assert doc.title == "第一章 背景"
    assert any(b.type == "heading" for b in doc.blocks)


def test_csv_parser():
    doc = CsvParser().parse("a,b\n1,2\n".encode("utf-8"), source="x.csv")
    assert len(doc.tables) == 1
    assert doc.tables[0].to_rows()[0] == ["a", "b"]


def test_html_parser():
    doc = HtmlParser().parse(b"<html><title>T</title><body><h1>H</h1><p>x</p></body></html>")
    assert doc.title == "T"
    assert len(doc.blocks) >= 2


def test_json_parser():
    doc = JsonParser().parse(b'{"title": "abc"}')
    assert doc.title == "abc"


def test_registry():
    exts = list_parsers()
    assert "pdf" in exts
    assert "docx" in exts
    assert "xlsx" in exts
    assert "html" in exts


def test_registry_parse_text():
    reg = get_registry()
    doc = reg.parse(b"hello world", ext="txt")
    assert doc.text == "hello world"

# -*- coding: utf-8 -*-
from docintel.output.renderer import render
from docintel.types import Block, Document, Table, TableCell


def _doc():
    d = Document(source="x", format="text", title="标题", text="正文")
    d.blocks = [Block(id="b0", type="heading", text="标题", level=1),
                Block(id="b1", type="paragraph", text="正文")]
    t = Table(id="t0", rows=[[TableCell(text="a"), TableCell(text="b")],
                             [TableCell(text="1"), TableCell(text="2")]])
    d.tables = [t]
    return d


def test_markdown():
    md = render(_doc(), "markdown")
    assert md.startswith("# 标题")
    assert "| a | b |" in md


def test_json():
    import json
    obj = json.loads(render(_doc(), "json"))
    assert obj["title"] == "标题"
    assert len(obj["tables"]) == 1


def test_html():
    html = render(_doc(), "html")
    assert "<h1>标题</h1>" in html


def test_csv():
    csv_out = render(_doc(), "csv")
    assert "a,b" in csv_out

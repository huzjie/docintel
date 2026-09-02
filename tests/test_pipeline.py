# -*- coding: utf-8 -*-
from docintel.config import load_config
from docintel.core.pipeline import Pipeline


def test_pipeline_text():
    cfg = load_config("nonexistent.json")
    pipe = Pipeline(cfg)
    data = "# 标题\n\n这是正文段落。\n\n- 列表一\n- 列表二\n".encode("utf-8")
    result = pipe.run(data, source="doc.txt", ext="txt")
    doc = result.document
    assert doc.format == "text"
    assert len(doc.blocks) >= 3
    assert len(doc.chunks) >= 1
    assert "parse: ok" in result.pipeline_log


def test_pipeline_markdown_output():
    cfg = load_config("nonexistent.json")
    pipe = Pipeline(cfg)
    result = pipe.run("# 标题\n正文\n".encode("utf-8"), source="a.md", ext="md")
    out = pipe.to_output(result, "markdown")
    assert "# 标题" in out

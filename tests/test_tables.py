# -*- coding: utf-8 -*-
from docintel.tables.grid import GridTableExtractor
from docintel.tables.heuristic import HeuristicTableExtractor


def test_grid_pipe():
    text = "a | b\n---|---\n1 | 2\n3 | 4"
    tables = GridTableExtractor().extract(text)
    assert len(tables) == 1
    assert tables[0].to_rows() == [["a", "b"], ["1", "2"], ["3", "4"]]


def test_grid_tab():
    text = "a\tb\n1\t2"
    tables = GridTableExtractor().extract(text)
    assert len(tables) == 1


def test_heuristic():
    lines = ["名称     数量", "苹果     10", "香蕉     20"]
    t = HeuristicTableExtractor().extract(lines)
    assert t is not None
    assert len(t.rows) == 3

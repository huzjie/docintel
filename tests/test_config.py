# -*- coding: utf-8 -*-
from docintel.config import load_config, DEFAULTS, _coerce, _deep_merge


def test_defaults():
    cfg = load_config("nonexistent.json")
    assert cfg["provider"] == "mock"
    assert cfg["pipeline"]["enable_layout"] is True


def test_deep_merge():
    a = {"x": {"y": 1, "z": 2}}
    b = {"x": {"y": 9}}
    assert _deep_merge(a, b)["x"] == {"y": 9, "z": 2}


def test_coerce():
    assert _coerce("true") is True
    assert _coerce("42") == 42
    assert _coerce("3.14") == 3.14
    assert _coerce("[a,b,c]") == ["a", "b", "c"]

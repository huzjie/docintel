# -*- coding: utf-8 -*-
from docintel.layout.rules import LayoutRules
from docintel.layout.block import classify_block


def test_cn_heading():
    assert classify_block("第三章 数据治理")[0] == "heading"


def test_num_heading():
    t, lvl = classify_block("1.2.3 详细设计")
    assert t == "heading"
    assert lvl == 3


def test_list_item():
    assert classify_block("- 列表项")[0] == "list_item"


def test_paragraph():
    assert classify_block("这是普通段落内容。")[0] == "paragraph"


def test_rules_classify():
    assert LayoutRules.classify("第二章 概述")[0] == "heading"

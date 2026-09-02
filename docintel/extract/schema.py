# -*- coding: utf-8 -*-
"""抽取 schema 定义。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class FieldSpec:
    """单个字段规格。"""
    name: str
    type: str = "string"          # string / int / float / bool / list / date / object
    description: str = ""
    required: bool = False


@dataclass
class ExtractionSchema:
    """抽取 schema：描述要从文档里抽哪些字段。"""
    name: str = "generic"
    description: str = ""
    fields: List[FieldSpec] = field(default_factory=list)

    @classmethod
    def invoice(cls):
        return cls(
            name="invoice",
            description="发票 / 单据抽取",
            fields=[
                FieldSpec("发票号码", "string", "发票唯一编号", True),
                FieldSpec("开票日期", "date", "开票日期"),
                FieldSpec("销售方名称", "string", "销售方 / 收款方"),
                FieldSpec("购买方名称", "string", "购买方 / 付款方"),
                FieldSpec("金额合计", "float", "含税合计金额"),
                FieldSpec("税额", "float", "税额"),
            ],
        )

    @classmethod
    def contract(cls):
        return cls(
            name="contract",
            description="合同抽取",
            fields=[
                FieldSpec("合同名称", "string", "合同标题", True),
                FieldSpec("甲方", "string", "甲方主体"),
                FieldSpec("乙方", "string", "乙方主体"),
                FieldSpec("签署日期", "date", "签署日期"),
                FieldSpec("合同金额", "float", "合同总金额"),
                FieldSpec("生效日期", "date", "生效日期"),
                FieldSpec("到期日期", "date", "到期日期"),
            ],
        )

    @classmethod
    def resume(cls):
        return cls(
            name="resume",
            description="简历抽取",
            fields=[
                FieldSpec("姓名", "string", "姓名", True),
                FieldSpec("学历", "string", "最高学历"),
                FieldSpec("工作年限", "string", "工作年限"),
                FieldSpec("技能", "list", "技能列表"),
                FieldSpec("最近公司", "string", "最近任职公司"),
            ],
        )


__all__ = ["FieldSpec", "ExtractionSchema"]

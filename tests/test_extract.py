# -*- coding: utf-8 -*-
from docintel.extract.schema import ExtractionSchema
from docintel.extract.prompts import build_extraction_prompt
from docintel.extract.llm_extractor import _parse_json
from docintel.providers.mock import MockProvider


def test_schema_invoice():
    s = ExtractionSchema.invoice()
    assert len(s.fields) == 6
    assert s.fields[0].required


def test_prompt():
    s = ExtractionSchema.contract()
    p = build_extraction_prompt(s, "合同内容")
    assert "合同名称" in p
    assert "JSON" in p


def test_parse_json_plain():
    assert _parse_json('{"a": 1}') == {"a": 1}


def test_parse_json_fenced():
    assert _parse_json('```json\n{"a": 2}\n```') == {"a": 2}


def test_mock_provider_extract():
    s = ExtractionSchema.contract()
    provider = MockProvider()
    from docintel.extract.llm_extractor import LlmExtractor
    from docintel.types import Document
    ex = LlmExtractor(provider, schema=s)
    doc = Document(source="x", format="text", text="甲乙双方签订本合同...")
    ex.extract(doc)
    assert len(doc.fields) > 0

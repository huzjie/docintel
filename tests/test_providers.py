# -*- coding: utf-8 -*-
from docintel.providers.mock import MockProvider
from docintel.providers.base import get_provider, list_providers


def test_mock_deterministic():
    m = MockProvider()
    a = m.complete("测试")
    b = m.complete("测试")
    assert a == b


def test_list_providers():
    assert "mock" in list_providers()
    assert "deepseek" in list_providers()


def test_get_provider_mock():
    p = get_provider({"provider": "mock", "providers": {}})
    assert p.name == "mock"

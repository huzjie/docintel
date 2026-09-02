# -*- coding: utf-8 -*-
from docintel.security.redact import PiiRedactor
from docintel.security.policy import SecurityPolicy
from docintel.errors import SecurityError
import pytest


def test_redact_phone():
    r = PiiRedactor()
    text, n = r.redact("联系人：13812345678")
    assert n >= 1
    assert "13812345678" not in text


def test_redact_email():
    r = PiiRedactor()
    text, n = r.redact("邮箱 abc@example.com")
    assert n >= 1
    assert "abc@example.com" not in text


def test_file_limit():
    p = SecurityPolicy(max_file_mb=1)
    with pytest.raises(SecurityError):
        p.check_file_size(2 * 1024 * 1024)

# -*- coding: utf-8 -*-
from docintel.parsers.email_parser import EmailParser


def test_email_parser():
    raw = ("From: a@x.com\nTo: b@x.com\nSubject: 测试邮件\n"
           "Content-Type: text/plain; charset=utf-8\n\n这是邮件正文。\n")
    doc = EmailParser().parse(raw.encode("utf-8"))
    assert doc.format == "email"
    assert doc.title == "测试邮件"
    assert "这是邮件正文" in doc.text

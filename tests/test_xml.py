# -*- coding: utf-8 -*-
from docintel.parsers.xml_parser import XmlParser


def test_xml_parser():
    xml = ("<project name=\"docintel\"><member><name>张三</name>"
           "<role>研发</role></member><member><name>李四</name>"
           "<role>产品</role></member></project>")
    doc = XmlParser().parse(xml.encode("utf-8"))
    assert doc.format == "xml"
    assert doc.title == "project"
    assert len(doc.tables) >= 1

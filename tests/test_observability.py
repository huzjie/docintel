# -*- coding: utf-8 -*-
from docintel.observability.metrics import Metrics
from docintel.observability.trace import TraceContext


def test_metrics():
    m = Metrics()
    m.inc("docs", 2)
    m.observe("latency", 10)
    out = m.render()
    assert "docintel_docs 2" in out


def test_trace():
    t = TraceContext()
    assert len(t.trace_id) == 32
    c = t.child()
    assert c.trace_id == t.trace_id
    assert c.span_id != t.span_id

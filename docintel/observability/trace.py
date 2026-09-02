# -*- coding: utf-8 -*-
"""W3C Trace Context（简化）。"""
from __future__ import annotations

import os
import random


class TraceContext:
    def __init__(self, trace_id: str = "", span_id: str = ""):
        self.trace_id = trace_id or _rand_hex(32)
        self.span_id = span_id or _rand_hex(16)

    def child(self) -> "TraceContext":
        return TraceContext(self.trace_id)

    def header(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-01"


def _rand_hex(n: int) -> str:
    return "%0*x" % (n, random.getrandbits(n * 4))


__all__ = ["TraceContext"]

# -*- coding: utf-8 -*-
"""简单 Prometheus 文本指标。"""
from __future__ import annotations

import time
from collections import defaultdict


class Metrics:
    def __init__(self):
        self._counters = defaultdict(float)
        self._hist = defaultdict(list)

    def inc(self, name: str, value: float = 1.0) -> None:
        self._counters[name] += value

    def observe(self, name: str, value: float) -> None:
        self._hist[name].append(value)

    def render(self) -> str:
        lines = []
        for k, v in sorted(self._counters.items()):
            lines.append(f"docintel_{k} {v}")
        for k, vals in sorted(self._hist.items()):
            if vals:
                avg = sum(vals) / len(vals)
                lines.append(f"docintel_{k}_avg {avg:.3f}")
                lines.append(f"docintel_{k}_count {len(vals)}")
        return "\n".join(lines) + "\n"


__all__ = ["Metrics"]

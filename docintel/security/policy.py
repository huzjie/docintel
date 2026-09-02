# -*- coding: utf-8 -*-
"""安全策略：文件大小 / 页数限制。"""
from __future__ import annotations

from dataclasses import dataclass

from ..errors import SecurityError


@dataclass
class SecurityPolicy:
    max_file_mb: float = 50.0
    max_pages: int = 500
    enable_pii_redact: bool = True

    def check_file_size(self, size_bytes: int) -> None:
        limit = int(self.max_file_mb * 1024 * 1024)
        if size_bytes > limit:
            raise SecurityError(f"文件 {size_bytes} 字节超过限制 {limit} 字节（{self.max_file_mb}MB）")


def enforce_file_limits(data: bytes, policy: SecurityPolicy) -> None:
    policy.check_file_size(len(data))


__all__ = ["SecurityPolicy", "enforce_file_limits"]

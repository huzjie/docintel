# -*- coding: utf-8 -*-
"""docintel Python SDK 便捷封装。"""
from __future__ import annotations

from docintel.config import load_config
from docintel.core.pipeline import Pipeline


class Docintel:
    """一个进程内复用的文档解析客户端。"""

    def __init__(self, config_path: str = "config.json"):
        self.config = load_config(config_path)
        self._pipe = Pipeline(self.config)

    def parse(self, data: bytes, source: str = "", ext: str = ""):
        """解析文档字节，返回 ParseResult。"""
        return self._pipe.run(data, source=source, ext=ext)

    def parse_file(self, path: str):
        return self._pipe.run_file(path)

    def to_markdown(self, result) -> str:
        return self._pipe.to_output(result, "markdown")

    def to_json(self, result) -> str:
        return self._pipe.to_output(result, "json")


__all__ = ["Docintel"]

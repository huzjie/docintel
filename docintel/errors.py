# -*- coding: utf-8 -*-
"""docintel 统一异常体系。"""


class DocintelError(Exception):
    """基础异常。"""


class ConfigError(DocintelError):
    """配置加载 / 校验错误。"""


class UnsupportedFormatError(DocintelError):
    """不支持的文件格式。"""


class ParseError(DocintelError):
    """文档解析失败。"""


class LayoutError(DocintelError):
    """版面分析失败。"""


class TableError(DocintelError):
    """表格抽取失败。"""


class OcrError(DocintelError):
    """OCR 识别失败。"""


class ExtractError(DocintelError):
    """LLM 结构化抽取失败。"""


class ProviderError(DocintelError):
    """LLM Provider 调用错误。"""


class StorageError(DocintelError):
    """存储层错误。"""


class SecurityError(DocintelError):
    """安全策略拒绝。"""


__all__ = [
    "DocintelError", "ConfigError", "UnsupportedFormatError", "ParseError",
    "LayoutError", "TableError", "OcrError", "ExtractError",
    "ProviderError", "StorageError", "SecurityError",
]

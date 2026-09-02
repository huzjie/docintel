# -*- coding: utf-8 -*-
"""配置加载：内置默认值 -> config.json 覆盖 -> DOCINTEL_* 环境变量覆盖。

零第三方依赖。环境变量名用双下划线表示层级，例如：:

    DOCINTEL_PROVIDER=mock
    DOCINTEL_PROVIDERS__OPENAI__API_KEY=sk-...
    DOCINTEL_PIPELINE__ENABLE_OCR=true
    DOCINTEL_SECURITY__MAX_FILE_MB=50
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from .errors import ConfigError

DEFAULTS: Dict[str, Any] = {
    "provider": "mock",
    "providers": {
        "openai": {"api_key": "", "base_url": "https://api.openai.com/v1", "model": "gpt-4o-mini"},
        "anthropic": {"api_key": "", "base_url": "https://api.anthropic.com", "model": "claude-sonnet-4-5"},
        "gemini": {"api_key": "", "base_url": "https://generativelanguage.googleapis.com", "model": "gemini-2.0-flash"},
        "deepseek": {"api_key": "", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
        "qwen": {"api_key": "", "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-plus"},
        "ollama": {"base_url": "http://localhost:11434", "model": "qwen2.5:7b"},
        "mock": {},
    },
    "pipeline": {
        "enable_layout": True,
        "enable_table": True,
        "enable_ocr": True,
        "enable_chunk": True,
        "enable_extract": False,
        "chunk_size": 800,
        "chunk_overlap": 120,
        "output_formats": ["markdown", "json"],
    },
    "ocr": {
        "engine": "mock",
        "tesseract_cmd": "tesseract",
        "lang": "chi_sim+eng",
    },
    "extract": {
        "max_tokens": 2048,
        "temperature": 0.0,
        "retries": 2,
    },
    "security": {
        "max_file_mb": 50,
        "max_pages": 500,
        "enable_pii_redact": True,
        "pii_placeholder": "[REDACTED]",
    },
    "storage": {
        "type": "sqlite",
        "path": ".docintel/data.db",
        "cache_dir": ".docintel/cache",
    },
    "server": {
        "host": "127.0.0.1",
        "port": 8000,
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _coerce(value: str) -> Any:
    """把环境变量字符串粗略转成 bool/int/float/list。"""
    v = value.strip()
    if v.lower() in ("true", "yes", "1", "on"):
        return True
    if v.lower() in ("false", "no", "0", "off"):
        return False
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"').strip("'") for x in inner.split(",")]
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def _env_override(cfg: Dict[str, Any], prefix: str = "DOCINTEL") -> Dict[str, Any]:
    for key, val in os.environ.items():
        if not key.startswith(prefix + "_"):
            continue
        parts = key[len(prefix) + 1:].split("__")
        cur = cfg
        for part in parts[:-1]:
            part = part.lower()
            if part not in cur or not isinstance(cur[part], dict):
                cur[part] = {}
            cur = cur[part]
        cur[parts[-1].lower()] = _coerce(val)
    return cfg


def load_config(path: str = "config.json", env_prefix: str = "DOCINTEL") -> Dict[str, Any]:
    """加载配置：默认 -> 文件 -> 环境变量。"""
    import copy
    cfg = copy.deepcopy(DEFAULTS)
    p = Path(path)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                cfg = _deep_merge(cfg, json.load(f))
        except (json.JSONDecodeError, OSError) as e:
            raise ConfigError(f"config 文件解析失败: {e}") from e
    cfg = _env_override(cfg, env_prefix)
    return cfg


__all__ = ["DEFAULTS", "load_config", "_deep_merge", "_coerce"]

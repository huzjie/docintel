# -*- coding: utf-8 -*-
"""Provider 基类与工厂。"""
from __future__ import annotations

import json
import urllib.request
from typing import Dict, List, Optional

from ..errors import ProviderError


class BaseProvider:
    """LLM Provider 基类。

    默认实现为 OpenAI 兼容 Chat Completions 协议，绝大多数自托管 / 云服务
    （DeepSeek/Qwen/Ollama/vLLM/OpenRouter）都可用同一套 HTTP 调用。
    """

    name = "base"

    def __init__(self, api_key: str = "", base_url: str = "", model: str = ""):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def complete(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.0) -> str:
        url = self.base_url + "/chat/completions"
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        req = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", "Bearer " + self.api_key)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"{self.name} 调用失败: {e}") from e
        try:
            return resp["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise ProviderError(f"{self.name} 响应解析失败: {resp}") from e


class AnthropicProvider(BaseProvider):
    """Anthropic Messages 协议。"""

    name = "anthropic"

    def complete(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.0) -> str:
        url = self.base_url + "/v1/messages"
        body = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("x-api-key", self.api_key)
        req.add_header("anthropic-version", "2023-06-01")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            raise ProviderError(f"anthropic 调用失败: {e}") from e
        try:
            return "".join(c.get("text", "") for c in resp["content"])
        except (KeyError, IndexError) as e:
            raise ProviderError(f"anthropic 响应解析失败") from e


def _build(provider: str, cfg: dict) -> BaseProvider:
    p = cfg.get("providers", {}).get(provider, {}) if isinstance(cfg.get("providers"), dict) else {}
    if provider == "anthropic":
        return AnthropicProvider(p.get("api_key", ""), p.get("base_url", ""), p.get("model", ""))
    if provider == "mock":
        from .mock import MockProvider
        return MockProvider()
    return BaseProvider(p.get("api_key", ""), p.get("base_url", ""), p.get("model", ""))


def get_provider(config: dict, name: Optional[str] = None) -> BaseProvider:
    name = name or config.get("provider", "mock")
    return _build(name, config)


def list_providers() -> List[str]:
    return ["openai", "anthropic", "gemini", "deepseek", "qwen", "ollama", "mock"]


__all__ = ["BaseProvider", "AnthropicProvider", "get_provider", "list_providers"]

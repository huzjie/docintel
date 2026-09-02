# -*- coding: utf-8 -*-
"""LLM Provider 适配器。"""
from .base import BaseProvider, get_provider, list_providers
from .mock import MockProvider

__all__ = ["BaseProvider", "get_provider", "list_providers", "MockProvider"]

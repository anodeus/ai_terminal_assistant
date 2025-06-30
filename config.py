
"""config.py
Config loader and LLM client factory.
"""
from __future__ import annotations
import pathlib, os
from typing import Any, Dict, Tuple

import yaml

# Optional LLM back‑ends
try:
    import google.generativeai as genai  # type: ignore
except ImportError:
    genai = None

try:
    from openai import OpenAI  # type: ignore[attr-defined]
except ImportError:
    OpenAI = None  # type: ignore

CONFIG_PATH = pathlib.Path.home() / ".ait.yml"

def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        return yaml.safe_load(CONFIG_PATH.read_text()) or {}
    return {}

CONFIG = load_config()

def get_llm_client() -> Tuple[str | None, Any | None, str | None]:
    """Return (backend_name, client_obj, model_name) or (None, None, None)."""
    if genai and CONFIG.get("gemini_api_key"):
        genai.configure(api_key=CONFIG["gemini_api_key"])
        return "gemini", genai, CONFIG.get("gemini_model", "gemini-1.5-flash")
    if OpenAI and CONFIG.get("openai_api_key"):
        client = OpenAI(api_key=CONFIG["openai_api_key"], base_url=CONFIG.get("openai_base_url"))
        return "openai", client, CONFIG.get("openai_model", "gpt-3.5-turbo")
    return None, None, None

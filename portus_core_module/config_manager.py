# portus_core_module/config_manager.py

"""
Centralised access to `portus_api_config.json`, with clear errors if a
required key is missing.  Function names are preserved exactly so no
imports elsewhere break.
"""

import json
from pathlib import Path
from typing import Any, Dict

class ConfigError(RuntimeError):
    """Raised when an expected key is missing in the JSON config."""

def load_config() -> Dict[str, Any]:
    cfg_path = Path(__file__).resolve().parent / "config" / "portus_api_config.json"
    try:
        with cfg_path.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError as exc:
        raise ConfigError(f"Configuration file not found: {cfg_path}") from exc


CONFIG = load_config() 

def _expect(value: Any, dotted_key: str):
    if value is None:
        raise ConfigError(f"Missing required key `{dotted_key}` in config")
    return value

def get_provider_mode() -> str:
    return _expect(CONFIG.get("mode", {}).get("default_mode"), "mode.default_mode")


def get_provider_name() -> str:
    source = get_provider_mode()
    provider = CONFIG.get("mode", {}).get(source, {}).get("default_provider")
    return _expect(provider, f"mode.{source}.default_provider")

def get_model() -> str:
    source = get_provider_mode()
    provider = get_provider_name()
    try:
        return CONFIG["mode"][source][provider]["model"]
    except KeyError as exc:
        raise ConfigError(f"mode.{source}.{provider}.model missing") from exc


def get_model_url(feature: str = "base_url") -> str:
    source = get_provider_mode()
    provider = get_provider_name()
    url = CONFIG["mode"][source][provider].get(feature)
    return _expect(url, f"mode.{source}.{provider}.{feature}")

def get_system_prompt():
    return CONFIG.get("parameters", {}).get("system_prompt")


def get_parameters() -> Dict[str, Any]:
    provider = get_provider_name()
    glob = CONFIG.get("parameters", {}).get("global", {})
    per = CONFIG.get("parameters", {}).get(provider, {})
    return {**glob, **per}  


def get_context_limit():
    return get_parameters().get("n_ctx")

PROVIDER_MODE = get_provider_mode()
PROVIDER_NAME = get_provider_name()
MODEL = get_model()
BASE_URL = get_model_url("base_url")

SYSTEM_PROMPT = get_system_prompt()
PARAMETERS = get_parameters()

TEMPERATURE = PARAMETERS.get("temperature")
TOP_P = PARAMETERS.get("top_p")
TOP_K = PARAMETERS.get("top_k")
N_CTX = PARAMETERS.get("n_ctx")
MAX_TOKENS = PARAMETERS.get("max_tokens")
STREAM = PARAMETERS.get("stream")
TOOLS = PARAMETERS.get("tools")
TOOL_CHOICE = PARAMETERS.get("tool_choice")
RESPONSE_FORMAT = PARAMETERS.get("response_format")
STOP = PARAMETERS.get("stop")

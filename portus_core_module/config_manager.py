import json
from pathlib import Path
from typing import Any, Dict

class ConfigError(RuntimeError):
    pass

def load_config() -> Dict[str, Any]:
    cfg = Path(__file__).resolve().parent / "config" / "portus_api_config.json"
    try:
        with cfg.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError as exc:
        raise ConfigError(f"Configuration file not found: {cfg}") from exc

CONFIG = load_config()

def _expect(value: Any, dotted: str):
    if value is None:
        raise ConfigError(f"Missing required key `{dotted}` in config")
    return value

def get_provider_mode() -> str:
    return _expect(CONFIG.get("mode", {}).get("default_mode"), "mode.default_mode")

def get_provider_name() -> str:
    src = get_provider_mode()
    prov = CONFIG.get("mode", {}).get(src, {}).get("default_provider")
    return _expect(prov, f"mode.{src}.default_provider")

def get_model() -> str:
    src, prov = get_provider_mode(), get_provider_name()
    try:
        return CONFIG["mode"][src][prov]["model"]
    except KeyError as exc:
        raise ConfigError(f"mode.{src}.{prov}.model missing") from exc

def get_model_url(feature: str = "base_url") -> str:
    src, prov = get_provider_mode(), get_provider_name()
    url = CONFIG["mode"][src][prov].get(feature)
    return _expect(url, f"mode.{src}.{prov}.{feature}")

def get_system_prompt():
    return CONFIG["parameters"].get("system_prompt")

def get_openai_params() -> Dict[str, Any]:
    return CONFIG["parameters"].get("openai", {})

def get_additional_params() -> Dict[str, Any]:
    return CONFIG["parameters"].get("additional", {})

PROVIDER_MODE = get_provider_mode()
PROVIDER_NAME = get_provider_name()
MODEL = get_model()
BASE_URL = get_model_url("base_url")

SYSTEM_PROMPT = get_system_prompt()
PARAMETERS = get_openai_params()      
ADD_PARAMETERS = get_additional_params()

# --- values for cloud call -----------------------------------------
TEMPERATURE = PARAMETERS.get("temperature")
TOP_P = PARAMETERS.get("top_p")
STREAM = PARAMETERS.get("stream")
TOOLS = PARAMETERS.get("tools")
TOOL_CHOICE = PARAMETERS.get("tool_choice")
STORE = PARAMETERS.get("store")

# --- values for local context / models -----------------------------
N_CTX = ADD_PARAMETERS.get("n_ctx")
MAX_TOKENS = ADD_PARAMETERS.get("max_tokens")
TOP_K = ADD_PARAMETERS.get("top_k")
PRESENCE_PENALTY = ADD_PARAMETERS.get("presence_penalty")
FREQUENCY_PENALTY = ADD_PARAMETERS.get("frequency_penalty")

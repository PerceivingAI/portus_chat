# portus_config_module/config_manager.py

import sys, json, os
from pathlib import Path
from typing import Any, Dict
from portus_config_module.config_utils import candidate_dirs

class ConfigError(RuntimeError):
    pass

def load_config() -> Dict[str, Any]:
    for base in candidate_dirs():
        cfg_path = base / "portus_chat_config.json"
        if cfg_path.is_file():
            return json.loads(cfg_path.read_text(encoding="utf-8"))

    raise ConfigError(
        "Configuration file 'portus_chat_config.json' not found.\n"
        + "\n".join(f"  • {d}" for d in candidate_dirs())
    )

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
    return CONFIG["model_parameters"].get("system_prompt")

def get_openai_params() -> Dict[str, Any]:
    return CONFIG["model_parameters"].get("openai", {})

def get_additional_params() -> Dict[str, Any]:
    return CONFIG["model_parameters"].get("additional", {})

def get_grok_params() -> Dict[str, Any]:
    return CONFIG["model_parameters"].get("grok", {})

PROVIDER_MODE = get_provider_mode()
PROVIDER_NAME = get_provider_name()
MODEL = get_model()
BASE_URL = get_model_url("base_url")

SYSTEM_PROMPT = get_system_prompt()
PARAMETERS = get_openai_params()      
ADD_PARAMETERS = get_additional_params()
GROK_PARAMS = get_grok_params()

# --- values for cloud call -----------------------------------------
TEMPERATURE = PARAMETERS.get("temperature")
TOP_P = PARAMETERS.get("top_p")
STREAM = PARAMETERS.get("stream")
TOOLS = PARAMETERS.get("tools")
TOOL_CHOICE = PARAMETERS.get("tool_choice")
MAX_OUTPUT_TOKENS = PARAMETERS.get("max_output_tokens")
STORE = PARAMETERS.get("store")

# --- values for local context / models -----------------------------
N_CTX = ADD_PARAMETERS.get("n_ctx")
MAX_TOKENS = ADD_PARAMETERS.get("max_tokens")
TOP_K = ADD_PARAMETERS.get("top_k")
PRESENCE_PENALTY = ADD_PARAMETERS.get("presence_penalty")
FREQUENCY_PENALTY = ADD_PARAMETERS.get("frequency_penalty")

# --- storage parameters --------------------------------------------
def get_storage_path() -> Path:
    cfg = CONFIG.get("storage_parameters", {})
    raw = cfg.get("storage_path", "") or ""
    try:
        candidate = Path(raw).expanduser().resolve() if raw else None
    except Exception:
        candidate = None

    if not candidate or not candidate.is_dir():
        default = Path.home() / "Downloads"
        print(f"💡 No valid storage_path set — using default location: {default}")
        default.mkdir(parents=True, exist_ok=True)
        return default

    return candidate

STORAGE_PATH = get_storage_path()
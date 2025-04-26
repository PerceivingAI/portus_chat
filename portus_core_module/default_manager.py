# portus_core_module/default_manager.py

import json
from pathlib import Path

# These are your defaults exactly as you specified:
DEFAULT_CONFIG = {
  "config_id": "portus_chat_config",
  "mode": {
    "default_mode": "api",
    "api": {
      "default_provider": "openai",
      "openai": {
        "model": "gpt-4.1-nano-2025-04-14",
        "base_url": "https://api.openai.com/v1"
      },
      "gemini": {
        "model": "gemini-2.0-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
      },
      "grok": {
        "model": "grok-3-mini",
        "base_url": "https://api.x.ai/v1"
      }
    },
    "local": {
      "portus": { "model": None }
    }
  },
  "parameters": {
    "system_prompt": "You are a helpful assistant.",
    "openai": {
      "temperature": 0.7,
      "top_p": 1.0,
      "stream": True,
      "tools": [],
      "tool_choice": "auto",
      "max_output_tokens": 10240,
      "store": False
    },
    "grok": {
      "reasoning_effort": "low"
    },
    "additional": {
      "n_ctx": 10240,
      "max_tokens": 10240,
      "top_k": 40,
      "presence_penalty": 0.2,
      "frequency_penalty": 0.2
    }
  }
}


def reset_defaults(config_path: Path = None):
    """
    Overwrite the JSON config at `config_path` with DEFAULT_CONFIG.
    If `config_path` is omitted, assumes the file lives at:
      <repo_root>/portus_chat_config.json
    """
    if config_path is None:
        config_path = (
            Path(__file__).resolve().parents[1]  # up from default_manager → portus_core_module → repo root
            / "portus_chat_config.json"
        )
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"✅ Reset configuration to defaults at {config_path}")
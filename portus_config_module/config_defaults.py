# portus_config_module/default_manager.py

import json
import sys
import textwrap
from pathlib import Path
from typing import Optional
from portus_config_module.config_utils import candidate_dirs

# ——— JSON defaults ————————————————————————————————————————————————
DEFAULT_CONFIG_CONTENT = textwrap.dedent("""\
{
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
      "portus": { "model": null }
    }
  },

   "storage_parameters": {
    "storage_path": ""
  },

  "model_parameters": {
    "system_prompt": "You are a helpful assistant.",

    "openai": {
      "temperature": 0.7,
      "top_p": 1.0,
      "stream": true,
      "tools": [],
      "tool_choice": "auto",
      "max_output_tokens": 20480,
      "store": false
    },

    "grok": {
      "reasoning_effort": "low"
    },

    "additional": {
      "n_ctx": 512000,
      "max_tokens": 20480,
      "top_k": 40,
      "presence_penalty": 0.2,
      "frequency_penalty": 0.2
    }
  }
}""")

def reset_config_defaults(config_path: Optional[Path] = None):
    if config_path is None:
        for base in candidate_dirs():
            candidate = base / "portus_chat_config.json"
            if candidate.exists():
                config_path = candidate
                break
        else:
            config_path = next(candidate_dirs()) / "portus_chat_config.json"

    config_path.write_text(DEFAULT_CONFIG_CONTENT, encoding="utf-8")
    print(f"✅ Created default portus_chat_config.json at {config_path}")


# ——— ENV defaults ——————————————————————————————————————————————————

# The exact lines we want in a fresh .env
DEFAULT_ENV_CONTENT = textwrap.dedent("""\
# AI provider API keys (replace placeholders with real keys)

OPENAI_API_KEY=your-openai-api-key

GEMINI_API_KEY=your-gemini-api-key

GROK_API_KEY=your-grok-api-key
""")

def reset_env_defaults(env_path: Optional[Path] = None):
    if env_path is None:
        for base in candidate_dirs():
            candidate = base / ".env"
            if candidate.exists():
                env_path = candidate
                break
        else:
            env_path = next(candidate_dirs()) / ".env"

    env_path.write_text(DEFAULT_ENV_CONTENT, encoding="utf-8")
    print(f"✅ Created placeholder .env at {env_path}")
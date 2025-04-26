# api_module/api_factory.py

import os
from portus_core_module.config_manager import PROVIDER_NAME, MODEL, BASE_URL, STREAM
from .api_openai import OpenAIResponsesClient
from .api_gemini import GeminiClient

def get_client():
    api_key = os.getenv(f"{PROVIDER_NAME.upper()}_API_KEY")
    if not api_key:
        raise ValueError(f"API key for provider '{PROVIDER_NAME}' not found in environment variables.")

    if PROVIDER_NAME == "gemini":
        return GeminiClient(
            api_key=api_key,
            model=MODEL,
            base_url=BASE_URL,
            stream=STREAM
        )

    elif PROVIDER_NAME == "openai":
        return OpenAIResponsesClient(
            api_key=api_key,
            model=MODEL,
            base_url=BASE_URL,
            stream=STREAM
        )

    else:
        raise ValueError(f"Unsupported provider: {PROVIDER_NAME}")

def get_understanding_client():
    import os
    import google.genai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[get_understanding_client] ❌ Missing GEMINI_API_KEY in environment.")
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[get_understanding_client] ❌ Failed to initialize client: {e}")
        return None

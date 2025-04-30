# portus_api_module/api_grok.py

from openai import OpenAI
import httpx
from portus_config_module.config_manager import GROK_PARAMS

class GrokClient:
    """
    Chat Completion client pointed at xAI's GPT endpoint.
    Mirrors the OpenAI interface (chat.completions.create).
    """

    def __init__(self, api_key: str, model: str, base_url: str, stream: bool = False):
        self.model  = model
        self.stream = stream
        self._http  = httpx.Client()
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=self._http,
        )

    def chat(self, messages, **kwargs):
        # Remove parameters not accepted by the Grok endpoint
        kwargs.pop("max_output_tokens", None)

        kwargs.pop("tool_choice", None)
        
        reasoning = GROK_PARAMS.get("reasoning_effort")
        if reasoning:
            kwargs["reasoning_effort"] = reasoning

        # Adapt each message for Grok: wrap content text in the required array
        adapted = []
        for msg in messages:
            adapted.append({
                "role": msg["role"],
                "content": [{"type": "text", "text": msg["content"]}]
            })

        if not self.stream:
            return self.client.chat.completions.create(
                model=self.model,
                messages=adapted,
                **kwargs
            )

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=adapted,
            stream=True,
            **kwargs
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            text = getattr(delta, "content", "")
            if text:
                yield text

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

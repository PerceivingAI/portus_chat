# portus_api_module/api_gemini.py

from openai import OpenAI
import httpx


class GeminiClient:
    """
    Thin wrapper that lets us call Gemini through the OpenAI-python SDK.

    Adds `close()` and context-manager support so the underlying httpx
    connection pool is released when we’re done.
    """

    def __init__(self, api_key: str, model: str, base_url: str, stream: bool = False):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.stream = stream
        self._http = httpx.Client()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=self._http,
        )

    def chat(self, messages, tools=None, tool_choice="auto", **kwargs):
        """
        Forward to `openai-python` chat endpoint.
        """
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=self.stream,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs,
        )

    def close(self):
        """Close the internal httpx.Client to free sockets."""
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

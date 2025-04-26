from openai import OpenAI
import httpx

class GeminiClient:
    """
    Uses the OpenAI SDK pointed at Gemini’s REST endpoint.
    Supports streaming and non-streaming chat completions.
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
        """
        messages: List[{"role":..., "content":...}]
        kwargs: temperature, top_p, tools, tool_choice, max_output_tokens, etc.
        """
        # Remove parameters not accepted by the Gemini endpoint
        kwargs.pop("max_output_tokens", None)

        if not self.stream:
            # single-shot completion
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs,
            )
            # return stub with only content
            class _Stub: pass
            stub = _Stub()
            stub.choices = resp.choices  # keep full object if needed
            return stub

        # streaming branch
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **kwargs,
        )
        for chunk in stream:
            # OpenAI-style delta streaming
            delta = chunk.choices[0].delta
            text = getattr(delta, "content", "")
            if text:
                yield text

    def close(self):
        """Close the underlying HTTP pool."""
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

from openai import OpenAI
import httpx

class OpenAIResponsesClient:
    """Wrapper so the rest of the app can call .chat() transparently."""

    def __init__(self, api_key, model, base_url, stream=False):
        self.model = model
        self.stream = stream
        self._http  = httpx.Client()
        self.client = OpenAI(api_key=api_key,
                             base_url=base_url,
                             http_client=self._http)

    def chat(self, messages, **kwargs):
        stream = self.client.responses.create(
            model=self.model,
            input=messages,
            stream=True,
            **kwargs
        )

        for event in stream:
            if event.type == "response.created":
                continue

            if event.type == "response.output_text.delta":
                # delta is already the text fragment
                yield event.delta
                continue

            if event.type == "response.completed":
                return

            if event.type == "error":
                raise RuntimeError(f"Streaming error: {event.error}")

        # ignore all other semantic events




    def close(self):
        self._http.close()

    def __enter__(self): return self
    def __exit__(self, *a): self.close()

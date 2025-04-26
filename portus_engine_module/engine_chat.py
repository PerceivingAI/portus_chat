from portus_core_module.config_manager import (
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    BASE_URL,
    STREAM,
)

from portus_context_module.context_manager import ContextManager
from portus_context_module.context_adapters import (
    to_openai_format,
    to_gemini_native_format,
)

# Global context
context = ContextManager()
USING_OPENAI_STYLE = "openai" in BASE_URL.lower()

def _extract_content(resp):
    try:
        text = resp.output_text
        return text
    except AttributeError:
        print("[engine_chat] ⚠️ output_text missing, trying raw content…")
    try:
        first = resp.content[0]
        text = first.get("text")
        return text
    except Exception as e:
        print("[engine_chat] ❌ Failed to get text from resp.content:", e)
    raise RuntimeError("Cannot extract assistant content from response")


def chat_with_model(client, messages, tools=None, tool_choice="auto"):

    for msg in messages:
        context.add_turn(msg["role"], msg["content"])

    if USING_OPENAI_STYLE:
        formatted = to_openai_format(context.get_history())
    else:
        formatted = to_gemini_native_format(context.get_history())

    kwargs = {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "tools": tools,
        "tool_choice": tool_choice,
    }
  
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if STREAM:
        assistant_reply = ""

        def token_generator():
            nonlocal assistant_reply
            try:
                response = client.chat(messages=formatted, **kwargs)
                for chunk in response:
                    if hasattr(chunk, "choices"):
                        delta = chunk.choices[0].delta
                        token = getattr(delta, "content", "")
                    else:
                        token = str(chunk)
                    if token:
                        assistant_reply += token
                        yield token
            finally:
                if assistant_reply.strip():
                    context.add_turn("assistant", assistant_reply)

        return token_generator()

    response = client.chat(messages=formatted, **kwargs)
    assistant_reply = _extract_content(response)
    context.add_turn("assistant", assistant_reply)
    return assistant_reply

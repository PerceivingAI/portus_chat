# portus_engine_module/engine_chat.py

from portus_core_module.config_manager import (
    TEMPERATURE,
    TOP_P,
    TOP_K,
    MAX_TOKENS,
    BASE_URL,
    STREAM,
)

from portus_context_module.context_manager import ContextManager
from portus_context_module.context_adapters import (
    to_openai_format,
    to_gemini_native_format,
)

context = ContextManager()
USING_OPENAI_STYLE = "openai" in BASE_URL.lower()

def _extract_content(response_obj):
    """
    Return assistant text whether the provider is OpenAI-style or
    native Gemini.
    """
    try:
        return response_obj.choices[0].message.content
    except AttributeError:
        pass

    try:
        return response_obj.candidates[0].content.parts[0].text
    except AttributeError:
        raise RuntimeError("Cannot extract assistant content from response")

def chat_with_model(client, messages, tools=None, tool_choice="auto"):
    for msg in messages:
        context.add_turn(msg["role"], msg["content"])

    formatted_history = (
        to_openai_format(context.get_history())
        if USING_OPENAI_STYLE
        else to_gemini_native_format(context.get_history())
    )

    kwargs = {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "top_k": TOP_K,
        "tools": tools,
        "tool_choice": tool_choice,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if STREAM:
        assistant_reply = ""

        def token_generator():
            nonlocal assistant_reply
            try:
                response = client.chat(messages=formatted_history, **kwargs)
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        token = delta.content
                        assistant_reply += token
                        yield token
            finally:
                if assistant_reply.strip():
                    context.add_turn("assistant", assistant_reply)

        return token_generator()

    response = client.chat(messages=formatted_history, **kwargs)
    assistant_reply = _extract_content(response)
    context.add_turn("assistant", assistant_reply)
    return assistant_reply

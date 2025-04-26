# portus_context_module/context_adapters.py

def to_openai_format(history):
    """
    Converts internal history to OpenAI-compatible format.
    Returns a list of {"role": ..., "content": ...} messages.
    """
    formatted = []
    for entry in history:
        if "text" in entry:
            formatted.append({
                "role": entry["role"],
                "content": entry["text"]
            })
    return formatted


def to_gemini_native_format(history):
    """
    Converts internal history to Gemini native format.
    Returns a list of {"role": ..., "parts": [...]}
    """
    formatted = []
    for entry in history:
        if "text" in entry:
            formatted.append({
                "role": entry["role"],
                "parts": [entry["text"]]
            })
    return formatted

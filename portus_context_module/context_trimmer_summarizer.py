# portus_context_module/context_trimmer_summarizer.py

import os
from portus_api_module.api_factory import get_client

def trim_context(history, trim_ratio):
    """
    Trim the oldest messages from the history by the given ratio.
    This modifies the history in place and prints full debug output.

    Args:
        history (list): The complete message history.
        trim_ratio (float): Ratio of messages to trim from the start.
    """
    if not history:
        pass
        #print("[trimmer] 🟡 Empty history — skipping trim.")
        #return

    #print("\n[trimmer] ✂️ Trimming history...")

    # print("[trimmer] 📜 Full history before:")
    # for i, entry in enumerate(history):
    #     print(f"  {i+1:02d}. {entry['role']}: {entry['text'][:80]}")

    total_messages = len(history)
    trim_count = max(1, int(total_messages * trim_ratio))

    history[:] = history[trim_count:]  # Trim in place

    #print(f"[trimmer] 🗑️ Trimmed {trim_count} messages.")

    #print("[trimmer] ✅ Remaining history:")
    # for i, entry in enumerate(history):
    #     print(f"  {i+1:02d}. {entry['role']}: {entry['text'][:80]}")
    # print()

def summarize_context(history, summarize_ratio):
    if not history:
        pass
        #print("[summarizer] 🟡 Empty history — skipping summarization.")
        #return

    print("\n[summarizer] 📝 Summarizing history...")

    total_messages = len(history)
    summarize_count = max(2, int(total_messages * summarize_ratio))

    chunk = history[:summarize_count]
    remaining = history[summarize_count:]

    #print("\n[summarizer] 📜 Portion to summarize (RAW):")
    # for i, entry in enumerate(chunk):
    #     print(f"  {i+1:02d}. {entry['role']} → {repr(entry['text'])}")

    # Convert entire chunk to raw string
    prompt = "Summarize the following:\n\n" + "\n".join(entry["text"] for entry in chunk)

    #print("\n[summarizer] 📤 Prompt to model (RAW):")
    #print(repr(prompt))

    try:
        client = get_client()
        summary = ""

        #print("[summarizer] 📡 Sending summary request (stream=True)...")

        response = client.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512
        )

        print("[summarizer] 🔄 Receiving streamed tokens:")
        for chunk in response:
            delta = chunk.choices[0].delta
            token = getattr(delta, "content", "")
            #print(f"  [token] {repr(token)}")
            summary += token

        summary = summary.strip()
        if not summary:
            pass
            #print("[summarizer] ❌ Empty streamed summary.")
            #return

        summary_message = {
            "role": "assistant",
            "text": "[SUMMARY] " + summary
        }

        history[:] = [summary_message] + remaining

        #print("\n[summarizer] ✅ Final summary (RAW):")
        #print(repr(summary_message["text"]))

        # print("\n[summarizer] 🔁 History after summarization (RAW):")
        # for i, entry in enumerate(history):
        #      print(f"  {i+1:02d}. {entry['role']} → {repr(entry['text'])}")

    except Exception as e:
        pass
        #print(f"[summarizer] ❌ Failed to summarize: {e}")
        #return
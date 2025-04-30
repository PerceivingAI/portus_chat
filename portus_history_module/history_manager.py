# portus_history_module/history_manager.py

from typing import List, Dict
from portus_storage_module.storage_manager import list_conversations, load_conversation, delete_conversation

def get_index_entries() -> List[Dict]:
    return list_conversations()

def format_index(entries: List[Dict]) -> None:
    if not entries:
        print("No saved conversations.")
        return
    for i, ent in enumerate(entries, start=1):
        print(f"{i}) [{ent['last_access']}] “{ent['title']}”")

def remove_by_index(n: int) -> None:
    entries = get_index_entries()
    if 1 <= n <= len(entries):
        delete_conversation(entries[n-1]["id"])
        print(f"[HistoryManager] Deleted conversation {n}.")
    else:
        print("⚠️ Invalid index for deletion.")

def get_conversation_turns(n: int) -> (List[Dict], str):
    entries = get_index_entries()
    if not (1 <= n <= len(entries)):
        raise IndexError("Selection out of range")
    ent = entries[n-1]
    turns = load_conversation(ent["id"])
    return turns, ent["last_access"]

def format_conversation(turns: List[Dict]) -> None:
    for turn in turns:
        print(f"{turn['role'].capitalize()}: {turn['content']}")

def build_resume_payload(
    turns: List[Dict], last_access: str, new_message: str
) -> str:
    formatted_history = "\n".join(
        f"{t['role'].capitalize()}: {t['content']}" for t in turns
    )
    return (
        f"{formatted_history}\n"
        f"Last accessed: {last_access}\n\n"
        "Use the previous conversation history to continue the conversation, here is the next user message:\n"
        f"{new_message}"
    )
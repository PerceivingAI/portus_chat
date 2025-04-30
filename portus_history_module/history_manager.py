# portus_history_module/history_manager.py

from typing import List, Dict
from portus_storage_module.storage_manager import list_conversations, load_conversation, delete_conversation

def display_index(limit: int = 10) -> List[Dict]:
    entries = list_conversations(limit)
    if not entries:
        print("No saved conversations.")
        return []

    for i, ent in enumerate(entries, start=1):
        ts = ent["last_access"]
        title = ent["title"]
        print(f"{i}) [{ts}] “{title}”")
    return entries

def display_conversation_by_index(n: int, limit: int = 10):
    entries = list_conversations(limit)
    if not entries:
        print("No saved conversations.")
        return

    if n < 1 or n > len(entries):
        print(f"Invalid selection: {n}")
        return

    conv_id = entries[n-1]["id"]
    turns = load_conversation(conv_id)
    print(f"\n--- Conversation {n} (ID: {conv_id}) ---")
    for turn in turns:
        role = turn["role"]
        content = turn["content"]
        print(f"{role.capitalize()}: {content}")
    print("--- End of conversation ---\n")

def remove_by_index(n: int, limit: int = 10):
    entries = list_conversations(limit)
    conv_id = entries[n-1]["id"]
    delete_conversation(conv_id)
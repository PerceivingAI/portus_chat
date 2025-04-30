# portus_storage_module/storage_manager.py

from pathlib import Path
from portus_config_module.config_manager import STORAGE_PATH
from portus_storage_module.storage_lite import set_db_path, init_conversation, save_turn, list_conversations, load_conversation, delete_conversation

# internal current conversation ID
_current_conversation_id: str | None = None

def set_current_conversation_id(conv_id: str):
    """
    Set the conversation ID to reuse for resumed sessions.
    """
    global _current_conversation_id
    _current_conversation_id = conv_id

def get_current_conversation_id() -> str | None:
    """
    Retrieve the currently set conversation ID, if any.
    """
    return _current_conversation_id

# inject the path once
_storage_dir = STORAGE_PATH / "Portus_Chat_App_Storage"
_storage_dir.mkdir(parents=True, exist_ok=True)
_db_file = _storage_dir / "portus_chat_storage.db"
set_db_path(_db_file)

# expose unified API
def init_conversation_if_needed(first_message: str) -> str:
    """
    Create a new conversation if none set, otherwise return existing.
    """
    global _current_conversation_id
    if _current_conversation_id:
        return _current_conversation_id
    _current_conversation_id = init_conversation(first_message)
    return _current_conversation_id

def save_turn_for_conversation(conversation_id: str, role: str, content: str):
    save_turn(conversation_id, role, content)

def list_recent_conversations(limit: int = 10):
    return list_conversations(limit)

def load_conversation_by_id(conversation_id: str):
    return load_conversation(conversation_id)

def delete_conversation_by_id(conv_id: str):
    return delete_conversation(conv_id)
# portus_storage_module/storage_manager.py

from pathlib import Path
from portus_config_module.config_manager import STORAGE_PATH
from portus_storage_module.storage_lite import delete_conversation as _lite_delete

# choose which backend to use here:
from portus_storage_module.storage_lite import (
    set_db_path,
    init_conversation as _lite_init,
    save_turn as _lite_save,
    list_conversations as _lite_list,
    load_conversation as _lite_load,
)

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
_storage_dir = STORAGE_PATH / "Insight_App_Storage"
_storage_dir.mkdir(parents=True, exist_ok=True)
_db_file = _storage_dir / "portus_storage.db"
set_db_path(_db_file)

# expose unified API
def init_conversation(first_message: str) -> str:
    """
    Create a new conversation if none set, otherwise return existing.
    """
    global _current_conversation_id
    if _current_conversation_id:
        return _current_conversation_id
    _current_conversation_id = _lite_init(first_message)
    return _current_conversation_id

def save_turn(conversation_id: str, role: str, content: str):
    _lite_save(conversation_id, role, content)

def list_conversations(limit: int = 10):
    return _lite_list(limit)

def load_conversation(conversation_id: str):
    return _lite_load(conversation_id)

def delete_conversation(conv_id: str):
    return _lite_delete(conv_id)
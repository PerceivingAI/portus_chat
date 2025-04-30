# portus_context_module/context_manager.py

from portus_context_module.context_counter import is_above_threshold
from portus_storage_module.storage_manager import (
    init_conversation,
    save_turn,
    get_current_conversation_id,
)

# session-level storage flag (default on)
_storage_enabled = True

# instruction phrase used in the composite payload
_RESUME_INSTRUCTION = (
    "Use the previous conversation history to continue the conversation, here is the next user message:\n"
)

def set_storage_enabled(flag: bool):
    global _storage_enabled
    _storage_enabled = flag

class ContextManager:
    def __init__(self, max_turns=50):
        self.history = []
        self.max_turns = max_turns
        self.conversation_id = None
        self._initialized = False

    def add_turn(self, role, text, meta=None):
        if not text or not text.strip():
            print(f"[ContextManager] Skipped empty turn → role: {role!r}, text: {text!r}")
            return

        entry = {"role": role, "text": text.strip()}
        if meta:
            entry["meta"] = meta

        self.history.append(entry)
        self._enforce_turn_limit()

        if not _storage_enabled:
            return

        # FIRST USER TURN (new or resumed)
        if role == "user" and not self._initialized:
            # strip off the resume instruction if present
            if _RESUME_INSTRUCTION in text:
                new_msg = text.split(_RESUME_INSTRUCTION, 1)[1].strip()
            else:
                new_msg = text.strip()

            # reuse an existing conversation ID if set, otherwise create a new one
            existing = get_current_conversation_id()
            if existing:
                self.conversation_id = existing
            else:
                self.conversation_id = init_conversation(new_msg)

            save_turn(self.conversation_id, "user", new_msg)
            self._initialized = True
            return

        # SUBSEQUENT TURNS
        save_turn(self.conversation_id, role, text.strip())

    def get_history(self):
        return self.history

    def reset(self):
        self.history = []
        self.conversation_id = None
        self._initialized = False

    def _enforce_turn_limit(self):
        max_len = self.max_turns * 2
        if len(self.history) > max_len:
            self.history = self.history[-max_len:]

context = ContextManager()
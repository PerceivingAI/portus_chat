# portus_context_module/context_manager.py

from portus_context_module.context_counter import is_above_threshold
from portus_storage_module.storage_manager import init_conversation, save_turn, get_current_conversation_id

# Session-level storage flag, explicitly controlled per chat mode
_storage_enabled = True

_RESUME_INSTRUCTION = (
    "Use the previous conversation history to continue the conversation, here is the next user message:\n"
)

def set_storage_enabled(flag: bool):
    global _storage_enabled
    _storage_enabled = flag

class ContextManager:
    def __init__(self, max_turns=10000):
        self.history = []
        self.max_turns = max_turns
        self.conversation_id = None
        self._initialized = False

    def add_turn(self, role, text, meta=None):
        if not text or not text.strip():
            #print(f"[ContextManager] Skipped empty turn → role: {role!r}, text: {text!r}")
            return

        text = text.strip()
        entry = {"role": role, "text": text}
        if meta:
            entry["meta"] = meta

        self.history.append(entry)
        self._enforce_turn_limit()

        # Debug only — prints to stdout, never stored
        #print(f"[DEBUG] add_turn → initialized={self._initialized}, role={role}, text={text[:50]!r}")

        # Handle first user message
        if role == "user" and not self._initialized:
            self._initialized = True

            if _storage_enabled:
                if _RESUME_INSTRUCTION in text:
                    new_msg = text.split(_RESUME_INSTRUCTION, 1)[1].strip()
                else:
                    new_msg = text

                existing = get_current_conversation_id()
                self.conversation_id = existing or init_conversation(new_msg)
                save_turn(self.conversation_id, "user", new_msg)
            return

        # Save turn only if storage is enabled
        if _storage_enabled and self.conversation_id:
            save_turn(self.conversation_id, role, text)

    def get_history(self):
        return list(self.history)  # always return a copy

    def reset(self):
        self.history = []
        self.conversation_id = None
        self._initialized = False

    def _enforce_turn_limit(self):
        max_len = self.max_turns * 2
        if len(self.history) > max_len:
            self.history = self.history[-max_len:]

context = ContextManager()

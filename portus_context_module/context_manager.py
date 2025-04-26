# portus_context_module/context_manager.py

from portus_context_module.context_counter import is_above_threshold

class ContextManager:
    def __init__(self, max_turns=50):
        self.history = []
        self.max_turns = max_turns

    def add_turn(self, role, text, meta=None):
        if not text or not text.strip():
            print(f"[ContextManager] Skipped empty turn → role: {role!r}, text: {text!r}")
            return

        #print(f"[ContextManager] Adding turn → role: {role!r}, text: {text.strip()!r}")
        entry = {"role": role, "text": text.strip()}
        if meta:
            entry["meta"] = meta

        self.history.append(entry)
        self._enforce_turn_limit()

        # Check token threshold after each message
        # if is_above_threshold(self.history):
        #     print("[ContextManager] ⚠️ Context nearing limit. Trimming or summarization should trigger here.")


    def get_history(self):
        """
        Get the full message history.
        """
        return self.history

    def reset(self):
        """
        Clear the history.
        """
        self.history = []

    def _enforce_turn_limit(self):
        """
        Keeps the context size within allowed message pairs (turns).
        """
        max_len = self.max_turns * 2  # each turn = user + assistant
        if len(self.history) > max_len:
            self.history = self.history[-max_len:]

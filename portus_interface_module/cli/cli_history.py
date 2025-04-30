# portus_interface_module/cli/cli_history.py

import sys
from portus_interface_module.cli.cli_utils import handle_special_commands
from portus_history_module.history_manager import get_index_entries, format_index, remove_by_index, get_conversation_turns, build_resume_payload, format_conversation
from portus_storage_module.storage_manager import set_current_conversation_id
from portus_interface_module.cli.cli_chat import run_chat_mode
from portus_engine_module.engine_chat import chat_with_model
from portus_api_module.api_factory import get_client
from portus_config_module.config_manager import STREAM

MENU_NAME = "Conversation History"
MENU_ORDER = 2

def run_history_mode():
    print("📜 Conversation History mode. Type /exit to quit, /menu to return, or /delete N to remove.\n")

    entries = get_index_entries()
    format_index(entries)
    if not entries:
        return

    while True:
        sel = input("➤  ").strip()

        # deletion
        if sel.startswith("/delete"):
            parts = sel.split()
            if len(parts) == 2 and parts[1].isdigit():
                remove_by_index(int(parts[1]))
            else:
                print("⚠️ Usage: /delete <number>")
            return

        # exit/menu
        if not handle_special_commands(sel):
            return

        # selection
        try:
            idx = int(sel)
        except ValueError:
            print("⚠️ Please enter a valid number.")
            continue
        if idx < 1 or idx > len(entries):
            print("❌ Invalid selection.")
            continue
        break

    # show conversation
    turns, last_access = get_conversation_turns(idx)
    format_conversation(turns)
    print(f"\nLast accessed: {last_access}\n")

    # continuation prompt
    new_msg = input("🧑 You: ").strip()
    if not handle_special_commands(new_msg):
        return
    if not new_msg:
        print("⚠️ Empty input, returning to main menu.")
        return

    # resume storage
    set_current_conversation_id(entries[idx-1]["id"])

    # send composite
    payload = build_resume_payload(turns, last_access, new_msg)
    client = get_client()
    response = chat_with_model(client, [{"role": "user", "content": payload}])

    if STREAM:
        print("🤖 Assistant: ", end="", flush=True)
        for token in response:
            print(token, end="", flush=True)
        print()
    else:
        print(f"🤖 Assistant: {response}")

    # now normal chat
    run_chat_mode()
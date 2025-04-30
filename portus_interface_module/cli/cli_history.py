# portus_interface_module/cli/cli_history.py

import sys
from portus_interface_module.cli.cli_utils import handle_special_commands
from portus_history_module.history_manager import display_index, remove_by_index
from portus_storage_module.storage_manager import load_conversation, set_current_conversation_id
from portus_interface_module.cli.cli_chat import run_chat_mode
from portus_engine_module.engine_chat import chat_with_model
from portus_api_module.api_factory import get_client
from portus_config_module.config_manager import STREAM

MENU_NAME = "Conversation History"
MENU_ORDER = 2

def run_history_mode():
    print("📜 Conversation History mode. Type /exit to quit, /menu to return, or /delete N to remove.\n")

    entries = display_index()
    if not entries:
        return

    while True:
        sel = input("➤  ").strip()

        # deletion command
        if sel.startswith("/delete"):
            parts = sel.split()
            if len(parts) == 2 and parts[1].isdigit():
                n = int(parts[1])
                remove_by_index(n)
            else:
                print("⚠️ Usage: /delete <number>")
            return

        # handle /exit or /menu
        if not handle_special_commands(sel):
            return

        # parse number
        try:
            idx = int(sel)
        except ValueError:
            print("⚠️ Please enter a valid number.")
            continue

        # bounds check
        if idx < 1 or idx > len(entries):
            print("❌ Invalid selection.")
            continue

        break

    # 3) Display full conversation for reading
    conv_id = entries[idx-1]['id']
    turns = load_conversation(conv_id)
    for turn in turns:
        print(f"{turn['role'].capitalize()}: {turn['content']}")
    print(f"\nLast accessed: {entries[idx-1]['last_access']}\n")

    # 4) Prompt for continuation
    new_msg = input("🧑 You: ").strip()
    if not handle_special_commands(new_msg):
        return
    if not new_msg:
        print("⚠️ Empty input, returning to main menu.")
        return

    # 5) Prepare storage for resumed session
    set_current_conversation_id(conv_id)

    # 6) Build payload: history + instruction + new message
    formatted_history = "\n".join(
        f"{t['role'].capitalize()}: {t['content']}"
        for t in turns
    )
    payload = (
        f"{formatted_history}\n"
        f"Last accessed: {entries[idx-1]['last_access']}\n\n"
        "Use the previous conversation history to continue the conversation, here is the next user message:\n"
        f"{new_msg}"
    )

    # 7) Send the first composite message
    client = get_client()
    response = chat_with_model(client, [{"role": "user", "content": payload}])

    if STREAM:
        print("🤖 Assistant: ", end="", flush=True)
        for token in response:
            print(token, end="", flush=True)
        print()
    else:
        print(f"🤖 Assistant: {response}")

    # 8) Drop into the normal interactive loop
    run_chat_mode()

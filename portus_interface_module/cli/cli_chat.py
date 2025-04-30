# portus_interface_module/cli/cli_chat.py

from portus_engine_module.engine_chat import chat_with_model
from portus_config_module.config_manager import STREAM
from portus_api_module.api_factory import get_client
from portus_interface_module.cli.cli_utils import handle_special_commands
from portus_context_module.context_manager import set_storage_enabled, context
from portus_storage_module.storage_manager import set_current_conversation_id

MENU_NAME = "Contextual Chat"
MENU_ORDER = 1

def _chat_loop():
    client = get_client()
    print("💬 Chat mode activated. Type /exit to quit or /menu to return.\n")

    try:
        while True:
            prompt = input("🧑 You: ").strip()

            if not prompt:
                print("⚠️ Empty input, try again.")
                continue

            if not handle_special_commands(prompt):
                break  # force exit loop to trigger finally block

            messages = [{"role": "user", "content": prompt}]
            response = chat_with_model(client, messages)

            if STREAM:
                print("\n🤖 Assistant: ", end="", flush=True)
                for token in response:
                    print(token, end="", flush=True)
                print()
            else:
                print(f"\n🤖 Assistant: {response}")
    finally:
        context.reset()

def run_chat_mode():
    set_storage_enabled(True)
    context.reset()
    set_current_conversation_id(None)
    _chat_loop()
    context.reset()
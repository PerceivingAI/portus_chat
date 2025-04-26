# portus_interface_module/cli/cli_chat.py

import os
import sys
from dotenv import load_dotenv

from portus_engine_module.engine_chat import chat_with_model
from portus_core_module.config_manager import STREAM
from portus_api_module.api_factory import get_client
from portus_interface_module.cli.cli_utils import handle_special_commands

MENU_NAME = "Contextual Chat"
MENU_ORDER = 1

load_dotenv()


def run_chat_mode():
    client = get_client()
    print("💬 Chat mode activated. Type /exit to quit or /menu to return.\n")

    while True:
        prompt = input("🧑 You: ").strip()

        if not prompt:
            print("⚠️ Empty input, try again.")
            continue

        if not handle_special_commands(prompt):
            return          # go back to main menu

        messages = [{"role": "user", "content": prompt}]
        response = chat_with_model(client, messages)

        if STREAM:
            print("🤖 Assistant: ", end="", flush=True)
            for token in response:
                print(token, end="", flush=True)
            print()
        else:
            print(f"🤖 Assistant: {response}")

# portus_interface_module/cli/cli_utils.py

import sys

def handle_special_commands(user_input: str):
    """
    Checks for special commands like /exit or /menu and performs the action.

    Args:
        user_input (str): The input string from the user.

    Returns:
        bool: True if the main loop should continue, False otherwise.
    """
    cmd = user_input.strip().lower()
    if cmd == "/exit":
        print("👋 Exiting Portus.\n")
        sys.exit(0)
    elif cmd == "/menu":
        print("🔙 Returning to main menu.\n")
        return False
    return True

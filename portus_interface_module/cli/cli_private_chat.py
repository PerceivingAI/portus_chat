# portus_interface_module/cli/cli_private_chat.py

from portus_context_module.context_manager import set_storage_enabled
from portus_interface_module.cli.cli_chat import run_chat_mode

MENU_NAME = "Private Chat"
MENU_ORDER = 3

def run_private_mode():
    # disable storage for this session
    set_storage_enabled(False)
    # hand off to the exact same chat loop as Contextual Chat
    run_chat_mode()
    # re-enable storage afterward
    set_storage_enabled(True)

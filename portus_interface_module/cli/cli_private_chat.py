# portus_interface_module/cli/cli_private_chat.py

from portus_context_module.context_manager import set_storage_enabled, context
from portus_interface_module.cli.cli_chat import _chat_loop

MENU_NAME = "Private Chat"
MENU_ORDER = 3

def run_private_mode():
    global context
    set_storage_enabled(False)
    context.reset()
    _chat_loop()
    context.reset()
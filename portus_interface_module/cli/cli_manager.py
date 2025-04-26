# portus_interface_module/cli/cli_manager.py

import os
import importlib
from pathlib import Path
from collections import OrderedDict

CLI_FOLDER = Path(__file__).parent
EXCLUDED_FILES = {"cli_utils.py", "__init__.py", "cli_manager.py"}


def discover_cli_modes():
    mode_entries = []
    seen = set()          
    
    for file in os.listdir(CLI_FOLDER):
        if not file.endswith(".py") or file in EXCLUDED_FILES:
            continue

        module_name = file[:-3]
        import_path = f"portus_interface_module.cli.{module_name}"

        try:
            module = importlib.import_module(import_path)

            for attr in dir(module):
                if attr.startswith("run_") and attr.endswith("_mode"):
                    function = getattr(module, attr)
                    menu_name = getattr(module, "MENU_NAME", module_name.replace("cli_", "").capitalize())
                    menu_order = getattr(module, "MENU_ORDER", 9999)

                    key = (menu_name, function)
                    if key in seen:
                        continue

                    seen.add(key)
                    mode_entries.append((menu_order, menu_name, function))
        except Exception as e:
            print(f"[cli_manager] Failed to import {import_path}: {e}")

    sorted_modes = sorted(mode_entries, key=lambda x: (x[0], x[1]))
    return OrderedDict((name, func) for _, name, func in sorted_modes)


cli_modes = discover_cli_modes()

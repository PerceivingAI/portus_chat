# portus_interface_module/cli/cli_manager.py

import sys
import importlib
import pkgutil
from collections import OrderedDict
import portus_interface_module.cli as cli_pkg

def discover_cli_modes():
    mode_entries = []
    seen = set()

    # print(f"[cli_manager] Discovering in package: {cli_pkg.__name__}")

    # Iterate over all modules in the cli package, whether on disk or embedded
    for finder, module_name, ispkg in pkgutil.iter_modules(cli_pkg.__path__):
        import_path = f"{cli_pkg.__name__}.{module_name}"
        try:
            module = importlib.import_module(import_path)
            for attr in dir(module):
                if attr.startswith("run_") and attr.endswith("_mode"):
                    func = getattr(module, attr)
                    menu_name = getattr(module, "MENU_NAME", module_name.replace("cli_", "").capitalize())
                    menu_order = getattr(module, "MENU_ORDER", 9999)
                    key = (menu_name, func)
                    if key in seen:
                        continue
                    seen.add(key)
                    mode_entries.append((menu_order, menu_name, func))
        except Exception as e:
            print(f"[cli_manager] Failed to import {import_path}: {e}")

    mode_entries.sort(key=lambda x: (x[0], x[1]))
    return OrderedDict((name, func) for _, name, func in mode_entries)


cli_modes = discover_cli_modes()

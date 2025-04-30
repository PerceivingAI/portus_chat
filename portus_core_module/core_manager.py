# portus_config_module/app_manager.py

import sys
from pathlib import Path
import argparse

from portus_interface_module.cli.cli_manager import cli_modes
from portus_config_module.config_defaults import reset_config_defaults, reset_env_defaults

def show_menu():
    mode_names = list(cli_modes.keys())

    while True:
        print("\nWelcome to Portus! Please select a Mode:")
        for i, name in enumerate(mode_names, start=1):
            print(f"{i}. {name}")
        print(f"{len(mode_names)+1}. Exit")

        choice = input(f"➤  Enter choice (1-{len(mode_names)+1}): ").strip()

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(mode_names):
                cli_modes[mode_names[idx-1]]()
            elif idx == len(mode_names) + 1:
                print("👋 Exiting.")
                sys.exit(0)
            else:
                print("❌ Invalid selection.")
        else:
            print("❌ Please enter a number.")

def launch_portus():
    parser = argparse.ArgumentParser(description="Portus Modular Entry Point")
    parser.add_argument(
        "--reset-config",
        action="store_true",
        help="Reset insight_config.json to default values and exit"
    )
    parser.add_argument(
        "--reset-env",
        action="store_true",
        help="Create or overwrite .env with placeholder API keys and exit"
    )
    for name in cli_modes:
        parser.add_argument(
            f"--{name.lower()}",
            action="store_true",
            help=f"Launch {name} mode"
        )

    args = parser.parse_args()

    if args.reset_config:
        reset_config_defaults()
        return

    if args.reset_env:
        reset_env_defaults()
        return

    for name, func in cli_modes.items():
        if getattr(args, name.lower()):
            func()
            return

    show_menu()
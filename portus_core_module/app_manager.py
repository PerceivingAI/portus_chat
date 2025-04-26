# portus_core_module/app_manager.py

import argparse
import sys
from dotenv import load_dotenv

from portus_interface_module.cli.cli_manager import cli_modes

load_dotenv()

def show_menu():
    mode_names = list(cli_modes.keys())

    while True:
        print("\nWelcome to Portus! Please select a Mode:")
        for i, name in enumerate(mode_names, start=1):
            print(f"{i}. {name}")
        print(f"{len(mode_names)+1}. Exit")

        choice = input(f"➤  Enter choice (1-{len(mode_names)+1}): ").strip()

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(mode_names):
                mode_key = mode_names[index - 1]
                cli_modes[mode_key]()  # call the run_*_mode function
            elif index == len(mode_names) + 1:
                print("👋 Exiting.")
                sys.exit(0)
            else:
                print("❌ Invalid selection. Please try again.")
        else:
            print("❌ Invalid input. Please enter a number.")


def launch_portus():
    parser = argparse.ArgumentParser(description="Portus Modular Entry Point")

    for name in cli_modes:
        parser.add_argument(f"--{name.lower()}", action="store_true", help=f"Launch {name} mode")

    args = parser.parse_args()

    for name, func in cli_modes.items():
        if getattr(args, name.lower()):
            func()
            return

    show_menu()

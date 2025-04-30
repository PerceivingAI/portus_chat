# main.py

import sys, os
from pathlib import Path

from portus_config_module.config_validator import validate_or_create
from portus_config_module.config_utils import init_tiktoken_cache

validate_or_create()
init_tiktoken_cache()

from portus_core_module.core_manager import launch_portus

if __name__ == "__main__":
    launch_portus()
# portus_config_module/config_utils.py

import sys
import os
from pathlib import Path

def candidate_dirs():
    """Search order: CWD → script folder → frozen-exec temp dir."""
    yield Path.cwd()
    yield Path(sys.argv[0]).resolve().parent
    if getattr(sys, "frozen", False):
        yield Path(getattr(sys, "_MEIPASS", ""))

def init_tiktoken_cache():
    for base in candidate_dirs():
        cache_path = base / "tiktoken_cache"
        os.environ["TIKTOKEN_CACHE_DIR"] = str(cache_path)
        break


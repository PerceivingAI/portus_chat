# prep_tiktoken_cache.py
import requests
from pathlib import Path

URL = "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken"
dst_dir = Path(__file__).resolve().parent / "tiktoken_cache"
dst_dir.mkdir(exist_ok=True)
dst_file = dst_dir / "cl100k_base.tiktoken"

print(f"[prep] downloading {URL}")
with requests.get(URL, stream=True, timeout=30) as r:
    r.raise_for_status()
    with dst_file.open("wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print(f"[prep] saved to {dst_file}")

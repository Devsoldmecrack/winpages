import json
import os
import shutil
from datetime import datetime
from typing import List, Dict

APP_DIR = os.path.join(os.path.expanduser("~"), ".winpages")
DOCS_DIR = os.path.join(APP_DIR, "documents")
RECENTS_FILE = os.path.join(APP_DIR, "recents.json")

os.makedirs(APP_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

def _load() -> List[Dict]:
    if os.path.exists(RECENTS_FILE):
        try:
            with open(RECENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save(items: List[Dict]):
    with open(RECENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def touch_recent(path: str):
    items = _load()
    items = [i for i in items if i.get("path") != path]
    items.insert(0, {
        "path": path,
        "name": os.path.basename(path),
        "size": os.path.getsize(path) if os.path.exists(path) else 0,
        "ts": datetime.now().isoformat(timespec="minutes"),
    })
    _save(items[:50])


def remove_recent(path: str):
    items = _load()
    items = [i for i in items if i.get("path") != path]
    _save(items)


def list_recents() -> List[Dict]:
    return _load()


def app_documents_dir() -> str:
    return DOCS_DIR


def unique_path(basename: str, ext_preferred: str | None = None) -> str:
    name, ext = os.path.splitext(basename)
    if ext_preferred:
        ext = ext_preferred if ext_preferred.startswith('.') else f'.{ext_preferred}'
    candidate = os.path.join(DOCS_DIR, f"{name}{ext}")
    i = 1
    while os.path.exists(candidate):
        candidate = os.path.join(DOCS_DIR, f"{name} {i}{ext}")
        i += 1
    return candidate


def import_file(src_path: str) -> str:
    """Copy a file from anywhere into the app documents dir with unique naming, update recents, and return dest path."""
    if not os.path.exists(src_path):
        raise FileNotFoundError(src_path)
    base = os.path.basename(src_path)
    dest = unique_path(base)
    shutil.copy2(src_path, dest)
    touch_recent(dest)
    return dest

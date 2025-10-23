import os, sys

def resource_root() -> str:
    base = getattr(sys, '_MEIPASS', None)
    if base:
        return base
    # Fallback to project root (directory containing this file's parent)
    return os.path.dirname(os.path.dirname(__file__))


def asset_path(*relative: str) -> str:
    return os.path.join(resource_root(), *relative)

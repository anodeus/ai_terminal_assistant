"""
folder_search.py
Recursive folder finder.
"""
from __future__ import annotations
import pathlib
from typing import List

def find_folder(pattern: str, root: pathlib.Path = pathlib.Path.home()) -> List[pathlib.Path]:
    """Recursively search for folders starting with pattern under root."""
    return [p for p in root.rglob(f"{pattern}*") if p.is_dir()]

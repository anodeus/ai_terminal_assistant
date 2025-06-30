
"""file_search.py
Recursive file finder.
"""
from __future__ import annotations
import pathlib
from typing import List

def find_file(pattern: str, root: pathlib.Path = pathlib.Path.home()) -> List[pathlib.Path]:
    """Recursively search for files matching pattern under root."""
    return list(root.rglob(pattern))

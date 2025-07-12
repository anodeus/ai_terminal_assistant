# modules/file_utils.py

import os
import subprocess
import shutil

def open_file(path: str) -> str:
    """Open a file using available default application method."""
    full_path = os.path.expanduser(path.strip())

    if not os.path.exists(full_path):
        return f"[red]✖ File does not exist: {full_path}[/red]"

    # Priority list of openers
    openers = ["xdg-open", "gio open", "gnome-open", "kde-open", "exo-open"]

    for opener in openers:
        parts = opener.split()
        cmd = parts[0]
        if shutil.which(cmd):
            try:
                subprocess.Popen(parts + [full_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"[green]✔ Opened: {full_path}[/green]"
            except Exception as e:
                return f"[red]✖ Failed with {cmd}: {e}[/red]"

    return "[red]✖ No compatible file opener found (xdg-open, gio, etc.).[/red]"

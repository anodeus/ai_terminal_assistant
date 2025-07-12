# modules/tool_opener.py

import subprocess
import shutil
from modules import tools

GUI_NAMES = {
    "Wireshark": "wireshark",
    "GParted": "gparted",
    "Burp Suite": "burpsuite",
    "Firefox": "firefox",
    "Chromium": "chromium",
    "Nmap (Zenmap)": "zenmap",
}

def open_tool(command: str) -> bool:
    """Try to open a terminal or GUI tool by full command."""
    command = command.strip()

    # Split command for tool check (e.g., "wpscan --url ..." → "wpscan")
    toolname = command.split()[0]

    if tools.check_tool(toolname):
        try:
            terminal = (
                shutil.which("x-terminal-emulator")
                or shutil.which("gnome-terminal")
                or shutil.which("konsole")
            )

            if terminal:
                # Run command and keep shell open
                subprocess.Popen([terminal, "-e", f"bash -c '{command}; exec bash'"])
            else:
                subprocess.Popen(command.split())
            return True
        except Exception as e:
            print(f"Error launching terminal tool: {e}")
            return False

    # Fallback for GUI tools (only support basic names, not args)
    if shutil.which(toolname):
        try:
            subprocess.Popen(command.split())
            return True
        except Exception:
            return False

    return False

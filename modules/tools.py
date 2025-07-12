# modules/tools.py

import os
import glob
import shutil

COMMON_TERMINAL_TOOLS = [
    "nmap", "curl", "wget", "git", "python3", "pip", "docker", "netstat",
    "ifconfig", "tcpdump", "nc", "ssh", "gcc", "make", "whois", "dig",
    "traceroute", "iptables", "tmux", "htop", "top", "ufw", "firewalld"
]

def list_installed_terminal_tools() -> list[str]:
    """Return a sorted list of common terminal tools available in the PATH."""
    return sorted([tool for tool in COMMON_TERMINAL_TOOLS if shutil.which(tool)])

def list_installed_gui_apps() -> list[str]:
    """Return a sorted list of GUI application names by parsing .desktop files."""
    desktop_dirs = [
        "/usr/share/applications/",
        os.path.expanduser("~/.local/share/applications/")
    ]
    apps = set()
    for directory in desktop_dirs:
        if os.path.isdir(directory):
            for file in glob.glob(os.path.join(directory, "*.desktop")):
                try:
                    with open(file, encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("Name="):
                                app_name = line.strip().split("=", 1)[1]
                                apps.add(app_name)
                                break
                except Exception:
                    pass
    return sorted(apps)

def check_tool(name: str) -> bool:
    """Check if a given terminal tool is installed."""
    return shutil.which(name.strip()) is not None

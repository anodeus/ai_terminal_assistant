
"""process_scan.py
List and optionally inspect running processes.
"""
from __future__ import annotations
import psutil
from rich.console import Console
from dataclasses import dataclass

console = Console()

@dataclass
class ProcessInfo:
    pid: int
    name: str
    cmdline: str

def scan_processes(interactive: bool = False) -> None:
    """Print a table of running processes. If interactive, allow selecting PID for detail."""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            info = p.info
            procs.append(ProcessInfo(pid=info['pid'], name=info['name'] or '', cmdline=' '.join(info['cmdline'] or [])))
        except (psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Simple output
    for pi in procs:
        console.print(f"{pi.pid:>6} | {pi.name[:25]:25} | {pi.cmdline[:60]}")
    console.print(f"[green]{len(procs)} processes listed.[/green]")

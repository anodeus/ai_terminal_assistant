
"""diagnostics.py
Basic system health info using psutil.
"""
from __future__ import annotations
import psutil
from rich.console import Console

console = Console()

def sys_health() -> None:
    """Print battery, CPU, memory, disk usage."""
    console.print("[cyan]System Health[/cyan]")
    bat = psutil.sensors_battery()
    if bat:
        console.print(f"Battery: {bat.percent}% {'(Charging)' if bat.power_plugged else '(Discharging)'}")
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    console.print(f"CPU {cpu}% | MEM {mem.percent}% | DISK {disk.percent}%")

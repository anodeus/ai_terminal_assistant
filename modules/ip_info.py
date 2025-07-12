# modules/ip_info.py

import socket
import requests
import subprocess
import re

def get_private_ipv4() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unavailable"
    

def get_public_ipv4() -> str:
    try:
        ip = requests.get("https://api.ipify.org", timeout=3).text.strip()
        return ip
    except Exception:
        return "Unavailable"

def get_private_ipv6() -> str:
    try:
        output = subprocess.check_output(["ip", "-6", "addr"], encoding="utf-8")
        matches = re.findall(r"inet6 ([0-9a-f:]+)/\d+ scope global", output)
        return matches[0] if matches else "Not assigned"
    except Exception:
        return "Unavailable"

def get_public_ipv6() -> str:
    try:
        ip = requests.get("https://api64.ipify.org", timeout=3).text.strip()
        return ip if ":" in ip else "Not assigned"
    except Exception:
        return "Unavailable"

def get_gateway() -> str:
    try:
        output = subprocess.check_output(["ip", "route"], encoding="utf-8")
        match = re.search(r"default via ([\d\.]+)", output)
        if match:
            return match.group(1)
        return "Unavailable"
    except Exception:
        return "Unavailable"
    
def get_dns_servers() -> list[str]:
    dns_list = []
    try:
        with open("/etc/resolv.conf", "r") as f:
            for line in f:
                if line.startswith("nameserver"):
                    parts = line.strip().split()
                    if len(parts) == 2:
                        dns_list.append(parts[1])
    except Exception:
        pass
    return dns_list or ["Unavailable"]

def show_ip_info() -> str:
    dns_list = get_dns_servers()
    dns_str = ", ".join(dns_list)

    return (
        f"[blue]✔ Public IPv4:[/blue] {get_public_ipv4()}\n"
        f"[blue]✔ Public IPv6:[/blue] {get_public_ipv6()}"
        f"\n[cyan]✔ Private IPv4:[/cyan] {get_private_ipv4()}\n"
        f"[cyan]✔ Private IPv6:[/cyan] {get_private_ipv6()}\n"
        f"[green]✔ Gateway:[/green] {get_gateway()}\n"
        f"[magenta]✔ DNS:[/magenta] {dns_str}"
    )

def show_public_ip() -> str:
    return f"[blue]✔ Public IPv4:[/blue] {get_public_ipv4()}"

def show_private_ip() -> str:
    return f"[cyan]✔ Private IPv4:[/cyan] {get_private_ipv4()}"

def show_gateway() -> str:
    return f"[green]✔ Gateway:[/green] {get_gateway()}"

def show_dns() -> str:
    dns_list = get_dns_servers()
    dns_str = ", ".join(dns_list)
    return f"[magenta]✔ DNS:[/magenta] {dns_str}"

def show_ipv6_info() -> str:
    return (
        f"[blue]✔ Public IPv6:[/blue] {get_public_ipv6()}\n"
        f"[cyan]✔ Private IPv6:[/cyan] {get_private_ipv6()}"
    )

def show_ipv4_info() -> str:
    return (
        f"[blue]✔ Public IPv4:[/blue] {get_public_ipv4()}\n"
        f"[cyan]✔ Private IPv4:[/cyan] {get_private_ipv4()}"
    )

def show_public_ipv6() -> str:
    return f"[blue]✔ Public IPv6:[/blue] {get_public_ipv6()}"

def show_private_ipv6() -> str:
    return f"[cyan]✔ Private IPv6:[/cyan] {get_private_ipv6()}"

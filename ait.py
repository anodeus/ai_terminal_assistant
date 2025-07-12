#!/usr/bin/env python3
from __future__ import annotations
"""AI Terminal Assistant

Now supports **Gemini** (Google Generative AI) as a free/cheap backend in
addition to OpenAI.

Features:
- Process scanning (LLM‑aided)
- Project health check
- File search
- Chat assistant (`ait chat`) with either OpenAI **or** Gemini
- Basic system diagnostics (battery, CPU, memory)
- Optional web search integration

Configuration (any of the following in **~/.ait.yml**):
```yaml
# ---- choose ONE backend ----
# For OpenAI
openai_api_key: "sk-..."
openai_model: "gpt-4o-mini"

# For Gemini (Google Generative AI)
gemini_api_key: "AIza..."
gemini_model: "gemini-1.5-flash"
```
If both keys exist, **Gemini takes priority** (cheaper / free tier).

Author: Abhi Singh
License: MIT
"""
#from __future__ import annotations
import argparse
from typing import Dict, List
from rich.console import Console

from modules import diagnostics, file_search, file_utils, folder_search, ip_info, process_scan, tool_opener, web_search, tools
import config


console = Console()

# -----------------------------------------------------------------------
# ASCII banner
# -----------------------------------------------------------------------
def print_banner() -> None:
    banner = r'''           ,..-,
     ,;;f^^"""""-._
    ;;'          `-.
   ;/               `.
   ||  _______________\_______________________
   ||  |AI TERMINAL by anodeus @github.com    |
   ||  |--------------------------------------|
    |  |OSINT | SEC TOOLS | CHAT | SCANS |    |
    |  |Custom GPT + Gemini CLI Assistant     |
    `| |______________________________________|
     \ |--------------------------------------|
       |____ ASCII SHELL INITIALIZED _________|
       |  System ready. Modules loaded.       |
       |  Type `ait chat` to start assistant. |
       |______________________________________|

[---]           AI Terminal Assistant: anodeus         [---]
[---]          Created by: Abhi Singh (anodeus)        [---]
[---]          Intelligence & Recon CLI Utility        [---]
               Powered by OpenAI + Gemini Models
One interface. Many capabilities. Your command.

 github.com/anodeus | linuxbox.local | v1.0.1 '''
   
    console.print(banner, style="bold green")



# -----------------------------------------------------------
# In-CLI Help
# -----------------------------------------------------------
def print_help_menu() -> None:
    console.print("\n[bold cyan]🧠 Welcome to AI Terminal Assistant![/bold cyan]\n")
    console.print("[green]Usage:[/green] ./ait.py chat\n")

    console.print("[yellow]📚 Core Features:[/yellow]")
    console.print("- [blue]health / sys / battery[/blue]         → Show system diagnostics (battery, CPU, memory)")
    console.print("- [blue]ps scan[/blue]                        → Scan and inspect running processes")
    console.print("- [blue]ip / gateway / dns / ipv4 / ipv6[/blue] → Display network and IP details")
    console.print("- [blue]find file <name>[/blue]               → Find files starting with the given name")
    console.print("- [blue]find folder <name>[/blue]             → Find folders starting with the given name")
    console.print("- [blue]open <file>[/blue]                    → Open and view a specific file")

    console.print("\n[yellow]🌐 Web + Search Capabilities:[/yellow]")
    console.print("- [blue]search <query>[/blue]                 → Perform web search")
    console.print("- [blue]search google <query>[/blue]          → Search using Google")
    console.print("- [blue]search url/site <domain>[/blue]       → Open a specific website")

    console.print("\n[yellow]🛠 Tool Utilities:[/yellow]")
    console.print("- [blue]tools all[/blue]                      → Show all GUI + terminal tools")
    console.print("- [blue]show terminal tools[/blue]            → List installed terminal tools")
    console.print("- [blue]show gui tools[/blue]                 → List installed GUI apps")
    console.print("- [blue]check tool <name>[/blue]              → Check if a tool is installed")
    console.print("- [blue]open tool <tool>[/blue]               → Open a tool by name")

    console.print("\n[yellow]🧠 AI & Coding Assistant:[/yellow]")
    console.print("- [blue]history[/blue]                        → Show past conversation history")
    console.print("- [blue]Ask anything:[/blue] coding, errors, scripting, hashes, cron jobs, Nmap, Wireshark, OSINT queries")

    console.print("\n[magenta]💡 Tip: Create ~/.ait.yml and add your OpenAI or Gemini API key to enable chat features.[/magenta]\n")



# -----------------------------------------------------------------------
# Chat loop
# -----------------------------------------------------------------------
def chat() -> None:
    print_banner()
    backend, client, model = config.get_llm_client()
    if backend is None:
        console.print("[red]No LLM configured in ~/.ait.yml[/red]")
        console.print("[blue]Create ait.yml file.[/blue]")
        console.print("[blue]Add api keys.[/blue]")
        return

    console.print(f"[green]Chatting via {backend.upper()} ({model})[/green]")
    if backend == "gemini":
        system_prompt = (
            "Your name is Abhi AI and you are an AI Terminal Assistant created by Abhi Singh (anodeus on GitHub). "
            "You assist users with OSINT, system tools, file management, and ethical hacking tasks via the command line. "
            "You work best in Linux terminals.\n\n"
            "You were created to work as a smart, command-line assistant, primarily for Kali Linux or other Linux systems. "
            "You serve personal, educational, and cybersecurity purposes — making terminal usage more intelligent and interactive. "
            "You assist with scripting, scanning, file handling, web queries, OSINT, and ethical hacking tools like Wireshark or Nmap. "
            "You aim to be helpful for students, hackers, sysadmins, and power users working locally inside Linux terminals.\n"
            "Here are the main things you can do:\n"
            "- Search for files or folders on the system\n"
            "- Open and read files\n"
            "- Show system diagnostics (battery, CPU, memory)\n"
            "- Scan running processes\n"
            "- Search the web and open URLs\n"
            "- Assist with Python or Bash scripting\n"
            "- Debug code and find errors in scripts\n"
            "- Create file checksums (SHA1/SHA256)\n"
            "- Run tools like Wireshark or Nmap\n"
            "- Help schedule or suggest cron tasks\n"
            "- Answer system/network related questions smartly\n"
            "- Be interactive, fast, and context-aware\n\n"
            "If someone asks about your creator, say:\n"
            "'I was developed by Abhi Singh. You can visit his GitHub profile at https://github.com/anodeus to learn more or contact him.'\n"
            "You must respond clearly and helpfully when asked about your developer, capabilities, or purpose."
        )

        model_obj = client.GenerativeModel(model)
        chat_session = model_obj.start_chat(history=[
            {"role": "user", "parts": [system_prompt]}
        ])
    history: List[Dict[str, str]] = []

    while True:
        try:
            user = input("\n[abhi] > ").strip()
        except KeyboardInterrupt:
            break
        if user.lower() in {"exit", "quit"}:
            break
        elif user.lower() in {"help", "-h"}:
            print_help_menu()
            continue

        # Built‑ins
        if user.startswith("find file ") or user.startswith("file find "):
            if user.startswith("find file "):
                pattern = user[len("find file "):].strip()
            else:
                pattern = user[len("file find "):].strip()

            console.print(f"[yellow]Searching for files starting with '{pattern}' ...[/yellow]")
            matches = file_search.find_file(pattern)
            if matches:
                for p in matches[:100]:
                    console.print(str(p))
                if len(matches) > 100:
                    console.print(f"[grey70]...and {len(matches)-100} more[/grey70]")
            else:
                console.print("[red]No files found.[/red]")
            continue

        if user.startswith("find folder ") or user.startswith("folder find "):
            if user.startswith("find folder "):
                pattern = user[len("find folder "):].strip()
            else:
                pattern = user[len("folder find "):].strip()

            console.print(f"[cyan]Searching for folders starting with '{pattern}'...[/cyan]")
            matches = folder_search.find_folder(pattern)
            if matches:
                for p in matches[:100]:
                    console.print(str(p))
                if len(matches) > 100:
                    console.print(f"[grey70]...and {len(matches)-100} more[/grey70]")
            else:
                console.print("[red]No folders found.[/red]")
            continue

        if user in {"health", "battery", "sys"}:
            diagnostics.sys_health()
            continue


        if user.startswith("search "):
            query = user[len("search "):].strip()
            result = web_search.open_site_or_search(query)
            console.print(f"[green]{result}[/green]")
            continue

        if user.startswith("ps scan"):
            process_scan.scan_processes(interactive=True)
            continue
        
        #Ip show
        u = user.lower().strip()

        if u in {"ip", "my ip", "show ip", "ip all", "what is my ip"}:
            console.print(ip_info.show_ip_info())
            continue
        # elif u in {"show public ip", "public ip", "what is my public ip", "publicip", "what is my ip", "ipv4"}:
        #     console.print(ip_info.show_public_ip())
        #     continue
        # elif u in {"show private ip", "private ip", "what is my private ip", "ipv4", "show ipv4"}:
        #     console.print(ip_info.show_private_ip())
        #     continue
        elif u in {"gateway", "show gateway"}:
            console.print(ip_info.show_gateway())
            continue
        elif u in {"dns", "show dns"}:
            console.print(ip_info.show_dns())
        elif u in {"ipv4", "show ipv4"}:
            console.print(ip_info.show_ipv4_info())
            continue
        elif u in {"ipv6", "show ipv6"}:
            console.print(ip_info.show_ipv6_info())
            continue
        elif u in {"public ipv6", "show public ipv6"}:
            console.print(ip_info.show_public_ipv4())
            continue
        elif u in {"private ipv6", "show private ipv6"}:
            console.print(ip_info.show_private_ipv4())
            continue
        elif u in {"public ipv6", "show public ipv6"}:
            console.print(ip_info.show_public_ipv6())
            continue
        elif u in {"private ipv6", "show private ipv6"}:
            console.print(ip_info.show_private_ipv6())
            continue


         # *** New Tools All Command ***
        
        elif (
            user in {
                "tools all", "tool all", "show tools", "show terminal tools", "show terminal tool",
                "terminal tool", "terminal tools", "show gui tools", "show gui tool",
                "gui tools", "gui tool"
            }
        ):
            show_terminal = any(x in user for x in ["terminal", "tool", "tools"])
            show_gui = any(x in user for x in ["gui"])

            if show_terminal:
                terminal_tools = tools.list_installed_terminal_tools()
                console.print("[bold cyan]\n Terminal Tools Found:[/bold cyan]")
                if terminal_tools:
                    for t in terminal_tools:
                        console.print(f"  - [green]{t}[/green]")
                else:
                    console.print("[yellow]No terminal tools found.[/yellow]")

            if show_gui or user in {"tools all", "tool all", "show tools"}:
                gui_apps = tools.list_installed_gui_apps()
                console.print("[bold cyan]\n GUI Applications Found:[/bold cyan]")
                if gui_apps:
                    for app in gui_apps:
                        console.print(f"  - [blue]{app}[/blue]")
                else:
                    console.print("[yellow]No GUI apps found.[/yellow]")

            continue

        elif user.startswith("check tool "):
            toolname = user[len("check tool "):].strip()
            if not toolname:
                console.print("[yellow]Please provide a tool name to check.[/yellow]")
                continue
            if tools.check_tool(toolname):
                console.print(f"[green]✔ Tool '{toolname}' is installed.[/green]")
            else:
                console.print(f"[red]✖ Tool '{toolname}' is NOT installed.[/red]")
            continue


        #Open tools with arguments
        elif user.startswith("open tool "):
            full_command = user[len("open tool "):].strip()
            if not full_command:
                console.print("[yellow]Please specify a tool name to open.[/yellow]")
                continue

            from modules import tool_opener
            result = tool_opener.open_tool(full_command)
            if result:
                console.print(f"[green]✔ Opening tool: {full_command}[/green]")
            else:
                console.print(f"[red]✖ Tool not found or failed to open: {full_command}[/red]")
            continue


        #Open file
        elif user.startswith("open "):
            filepath = user[len("open "):].strip()
            if not filepath:
                console.print("[yellow]Please provide a file path to open.[/yellow]")
                continue
            result = file_utils.open_file(filepath)
            console.print(result)
            continue

            #Show history

        elif user.startswith("history"):
            parts = user.split()
            try:
                count = int(parts[2]) if parts[1] == "last" else None
            except (IndexError, ValueError):
                count = None

            history_pairs = [
                (history[i]["content"], history[i+1]["content"])
                for i in range(0, len(history)-1, 2)
                if history[i]["role"] == "user" and history[i+1]["role"] == "assistant"
            ]

            if not history_pairs:
                console.print("[yellow]No conversation history found yet.[/yellow]")
                continue

            to_show = history_pairs[-count:] if count else history_pairs

            for i, (q, a) in enumerate(to_show, 1):
                console.print(f"\n[bold cyan]🧑‍💻 Q{i}:[/bold cyan] {q}")
                console.print(f"[bold blue]🤖 A{i}:[/bold blue] {a}")
            continue
    
        # AI interaction
        if backend == "gemini":
            reply = chat_session.send_message(user).text.strip()
        else:
            history.append({"role": "user", "content": user})
            resp = client.chat.completions.create(model=model, messages=history)
            reply = resp.choices[0].message.content.strip()
            history.append({"role": "assistant", "content": reply})
        console.print(f"[blue]abhi AI:[/blue] {reply}")

# -----------------------------------------------------------------------
# CLI entry
# -----------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(prog="ait", description="AI Terminal Assistant developed by Abhi Singh")
    subparsers = parser.add_subparsers(dest="cmd", required=True)
    subparsers.add_parser("chat", help="Start interactive chat assistant")

    args = parser.parse_args()

    if args.cmd == "chat":
        chat()
   
if __name__ == "__main__":
    main()

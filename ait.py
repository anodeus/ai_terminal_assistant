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

from modules import diagnostics, file_search, file_utils, folder_search, web_search, tools, process_scan
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
    console.print("[yellow]Once inside the chat, try these commands:[/yellow]\n")
    console.print("- [blue]health/sys/battery[/blue]            → Show system diagnostics")
    console.print("- [blue]ps scan[/blue]                       → Scan running processes")
    console.print("- [blue]find file <name>[/blue]              → Find files starting with name")
    console.print("- [blue]find folder <name>[/blue]            → Find folders starting with name")
    console.print("- [blue]search <query>[/blue]                → Search the web")
    console.print("- [blue]search google <query>[/blue]         → Search using google web")
    console.print("- [blue]search url/site <query>[/blue]       → Enter the site github.com")
    console.print("- [blue]exit / quit[/blue]                   → Leave the assistant\n")
    console.print("[magenta]Create ~/.ait.yml with your OpenAI or Gemini key to enable chat features.[/magenta]")



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
        chat_session = client.GenerativeModel(model).start_chat()
    history: List[Dict[str, str]] = []

    while True:
        try:
            user = input("[abhi] > ").strip()
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
        console.print(f"[blue]AI:[/blue] {reply}")

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

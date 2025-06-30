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

from modules import diagnostics, file_search, web_search, process_scan
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

 github.com/anodeus | linuxbox.local | v1.0.0 '''
   
    console.print(banner, style="bold green")

# -----------------------------------------------------------------------
# Chat loop
# -----------------------------------------------------------------------
def chat() -> None:
    print_banner()
    backend, client, model = config.get_llm_client()
    if backend is None:
        console.print("[red]No LLM configured in ~/.ait.yml[/red]")
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

        # Built‑ins
        if user.startswith("file find "):
            pattern = user[len("file find "):].strip()
            console.print(f"[yellow]Searching for '{pattern}' ...[/yellow]")
            matches = file_search.find_file(pattern)
            if matches:
                for p in matches[:100]:
                    console.print(str(p))
                if len(matches) > 100:
                    console.print(f"[grey70]...and {len(matches)-100} more[/grey70]")
            else:
                console.print("[red]No files found.[/red]")
            continue

        if user in {"health", "battery", "sys"}:
            diagnostics.sys_health()
            continue

        if user.startswith("search "):
            console.print("[yellow]Searching web...[/yellow]")
            console.print("[green]Web:[/green] " + web_search.web_search(user[7:].strip()))
            continue

        if user.startswith("ps scan"):
            process_scan.scan_processes(interactive=True)
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
    parser = argparse.ArgumentParser(prog="ait")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("chat", help="Interactive chat with AI")
    sub.add_parser("health", help="Show system health")
    sub.add_parser("ps", help="Scan running processes")
    s_web = sub.add_parser("search", help="Quick web search")
    s_web.add_argument("query", nargs=argparse.REMAINDER)

    s_find = sub.add_parser("find", help="Find files by pattern")
    s_find.add_argument("pattern")

    args = parser.parse_args()

    if args.cmd == "chat":
        chat()
    elif args.cmd == "health":
        diagnostics.sys_health()
    elif args.cmd == "ps":
        process_scan.scan_processes()
    elif args.cmd == "search":
        q = " ".join(args.query).strip()
        console.print(web_search.web_search(q))
    elif args.cmd == "find":
        for p in file_search.find_file(args.pattern):
            console.print(p)

if __name__ == "__main__":
    main()

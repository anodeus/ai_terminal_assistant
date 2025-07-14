
# AI Terminal Assistant


**AI Terminal** is a command-line AI utility developed by **Abhi Singh** (`@anodeus`).  
It acts as a lightweight assistant powered by OpenAI and Google Gemini — bundled with system tools like process scanning, diagnostics, file search, and optional web search.



## Tech Stack

**Client / CLI:** [Python 3.9+](https://www.python.org/), [Rich](https://rich.readthedocs.io), [argparse](https://docs.python.org/3/library/argparse.html)

**LLM Back‑ends:** [OpenAI API](https://platform.openai.com/), [Google AI Gemini](https://ai.google.dev/)

**System Utilities:** [psutil](https://pypi.org/project/psutil/), [requests](https://pypi.org/project/requests/), [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), [hashlib](https://docs.python.org/3/library/hashlib.html), [socket](https://docs.python.org/3/library/socket.html), [shutil](https://docs.python.org/3/library/shutil.html), [subprocess](https://docs.python.org/3/library/subprocess.html), [os](https://docs.python.org/3/library/os.html), [platform](https://docs.python.org/3/library/platform.html)


## Installation

Clone the project

```bash
  git clone https://github.com/anodeus/ai_terminal_assistant.git
```

Go to the project directory

```bash
  cd ai_terminal_assistant
```
Install dependencies

```bash
  ./install.sh 
```
Try `bash install.sh` if `./install.sh` not work

Run Assistant

```bash
  ait chat
```


## Manual

```python
python3 -m venv aienv
source aienv/bin/activate
pip install -r requirements.txt
chmod +x ait.py
./ait.py chat
```
Give permission to install dependencies if above command not work
```bash
  chmod +x install.sh
```
Try `bash install.sh` if `./install.sh` not work

## Configuration

You need to add your `API_KEY` to a file named .ait.yml inside your home directory:

```bash
  nano ~/.ait.yml
```
Then paste:
```bash
  # ~/.ait.yml

  gemini_api_key: "your‑gemini‑key"
  gemini_model: "gemini-1.5-flash"

  # default gemini

  #openai_api_key: "your‑openai‑key"
  #openai_model: "gpt-3.5-turbo"
```
    

## Environment Variables / Secrets

To run this project, you need to set the following API keys in your config file (`~/.ait.yml`):

| Variable           | Description                       |
|--------------------|-----------------------------------|
| `gemini_api_key`   | Required for Gemini support       |
| `openai_api_key`   | Required for OpenAI support       |
| *(Optional)*       | `openai_base_url`, `gemini_model`, `openai_model` |

These are stored in `~/.ait.yml`, not in a `.env` file.


## CLI Command Reference

| Command                                     | Description                                          | Example                         |
| ------------------------------------------- | ---------------------------------------------------- | ------------------------------- |
| `./ait.py chat`                             | Launch Abhi AI (interactive CLI assistant) using LLM | `./ait.py chat`                 |
| `health` / `battery` / `sys`                | Show system diagnostics (CPU, memory, battery, disk) | `health`                        |
| `show ps` / `ps scan`                       | List or scan running processes                       | `ps scan`                       |
| `ip` / `show ip` / `ipv4` / `ipv6`          | Show network info like IP, gateway, DNS              | `ipv4`                          |
| `find file <name>` / `file find <name>`     | Recursively search for files by name                 | `file find notes.txt`           |
| `open <file>`                               | Open and read/display contents of a file             | `open todo.txt`                 |
| `find folder <name>` / `folder find <name>` | Recursively search for folders by name               | `folder find Documents`         |
| `search <query>`                            | Perform DuckDuckGo web search                        | `search kali linux wifi crack`  |
| `search google <query>`                     | Perform Google web search                            | `search google kali metasploit` |
| `search url <site>` / `search site <site>`  | Open a specific website directly                     | `search site github.com`        |
| `tools all` / `show tools`                  | Show all terminal and GUI tools installed            | `tools all`                     |
| `terminal tools` / `show terminal tools`    | List installed terminal-based tools                  | `terminal tools`                |
| `gui tools` / `show gui tools`              | List installed graphical (GUI) applications          | `gui tools`                     |
| `check tool <name>`                         | Check if a specific tool is installed                | `check tool wireshark`          |
| `open tool <name>`                          | Run a tool with optional arguments                   | `open tool nmap`                |
| `history`                                   | Show full chat history                               | `history`                       |
| `history last <n>`                          | Show last `n` Q\&A responses from chat               | `history last 3`                |
| `exit` / `quit`                             | Exit Abhi AI chat assistant                          | `exit`                          |


> AI Terminal chooses **Gemini** when both Gemini and OpenAI keys are present in `~/.ait.yml` because Gemini’s free tier is cheaper.


##  FAQ

####  What if `./install.sh` fails?

This usually happens on distros like Kali or when `python3-venv` is missing.

**Fix:**  
Install venv and run the manual setup.

#### Where should I save `.ait.yml`?

You must save it in your **home directory**, not the project folder.

To create it:

```bash
nano ~/.ait.yml

```
##UNINSTALLING

To completely remove the assistant from your system, type:

```bash
uninstall
```
This will:

    Delete the virtual environment located at ~/.abhi_ai

    Remove the launcher (/usr/local/bin/ait)

    Ask whether to delete your API config file (~/.ait.yml)

    Remove the cloned project directory (~/abhi_ai)

 You will be prompted before anything important is deleted.
## Author

- [@anodeus](https://www.github.com/anodeus)


## License

[MIT](https://choosealicense.com/licenses/mit/)



# AI Terminal Assistant


**AI Terminal** is a command-line AI utility developed by **Abhi Singh** (`@anodeus`).  
It acts as a lightweight assistant powered by OpenAI and Google Gemini — bundled with system tools like process scanning, diagnostics, file search, and optional web search.



## Tech Stack

**Client / CLI:** Python 3.9+, [Rich](https://rich.readthedocs.io)

**LLM Back‑ends:** [OpenAI API](https://platform.openai.com/), [Google AI Gemini](https://ai.google.dev/)

**System Utilities:** [psutil](https://pypi.org/project/psutil/), [requests](https://pypi.org/project/requests/), [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)


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

Give execute permissions

```bash
  chmod +x ait.py
```

Run Assistant

```bash
  ./ait.py chat
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

| Command | Description | Example |
|---------|-------------|---------|
| `./ait.py chat` | Interactive chat with the configured LLM (Gemini or OpenAI) | `./ait.py chat` |
| `health` | Show system health (CPU, memory, battery, disk) | `health` |
| `show ps` | List running processes | `show ps` |
| `file find <pattern>` | Recursively search for files | `file find notes.txt` |
| `search <query>` | DuckDuckGo quick search | `search Kali Linux tips` |

| Command                                     | Description                                                 | Example                        |
| ------------------------------------------- | ----------------------------------------------------------- | ------------------------------ |
| `./ait.py chat`                             | Interactive chat with the configured LLM (Gemini or OpenAI) | `./ait.py chat`                |
| `health` / `battery` / `sys`                | Show system health (CPU, memory, battery, disk)             | `health`                       |
| `show ps` / `ps scan`                       | List or scan running processes                              | `ps scan`                      |
| `file find <name>` / `find file <name>`     | Recursively search for files by name                        | `file find notes.txt`          |
| `folder find <name>` / `find folder <name>` | Recursively search for folders by name                      | `folder find Documents`        |
| `search <query>`                            | DuckDuckGo search                                           | `search Kali Linux tips`       |
| `search google <query>`                     | Google search                                               | `search google kali wifi hack` |
| `search url <site>` / `search site <site>`  | Open a specific website                                     | `search url github.com`        |
| `tools all` / `show tools`                  | Show all terminal & GUI tools                               | `tools all`                    |
| `terminal tools` / `show terminal tools`    | Show terminal-based tools                                   | `terminal tools`               |
| `gui tools` / `show gui tools`              | Show GUI applications                                       | `gui tools`                    |
| `check tool <name>`                         | Check if a specific tool is installed                       | `check tool nmap`              |
| `open <file>`                               | Open and display contents of a file                         | `open todo.txt`                |
| `history`                                   | Show full chat history                                      | `history`                      |
| `history last <n>`                          | Show last `n` Q/A exchanges                                 | `history last 5`               |
| `exit` / `quit`                             | Exit the chat assistant                                     | `exit`                         |


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
## Author

- [@anodeus](https://www.github.com/anodeus)


## License

[MIT](https://choosealicense.com/licenses/mit/)


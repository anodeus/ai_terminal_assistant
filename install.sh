#!/bin/bash

# -------------------------------------------------------
# AI Terminal Installer
# Creates a local virtual environment named 'aienv'
# and installs dependencies from requirements.txt
# -------------------------------------------------------

echo "[*] Creating Python virtual ai_environment 'aienv'..."
python3 -m venv aienv || { echo "[!] Failed to create virtualenv."; exit 1; }

echo "[*] Activating 'aienv'..."
source aienv/bin/activate || { echo "[!] Failed to activate virtualenv."; exit 1; }

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing dependencies from requirements.txt..."
pip install -r requirements.txt || { echo "[!] pip install failed."; deactivate; exit 1; }

echo ""
echo "[+] Setup complete!"
echo "-------------------------------------------"
echo "To activate AI Terminal later, run:"
echo "  source aienv/bin/activate"
echo ""
echo "Make sure to add openAI or Gemini API key in ~/.ait.yml "
echo ""
echo "To start the assistant, run:"
echo "  ./ait.py chat"
echo "-------------------------------------------"

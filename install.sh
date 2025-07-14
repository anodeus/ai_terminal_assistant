#!/bin/bash

# -------------------------------------------------------
# AI Terminal Installer
# Creates a local virtual environment named 'aienv'
# and installs dependencies from requirements.txt
# -------------------------------------------------------

# echo "[*] Creating Python virtual ai_environment 'aienv'..."
# python3 -m venv aienv || { echo "[!] Failed to create virtualenv."; exit 1; }

# echo "[*] Activating 'aienv'..."
# source aienv/bin/activate || { echo "[!] Failed to activate virtualenv."; exit 1; }

# echo "[*] Upgrading pip..."
# pip install --upgrade pip

# echo "[*] Installing dependencies from requirements.txt..."
# pip install -r requirements.txt || { echo "[!] pip install failed."; deactivate; exit 1; }

# echo ""
# echo "[+] Setup complete!"
# echo "-------------------------------------------"
# echo "To activate AI Terminal later, run:"
# echo "  source aienv/bin/activate"
# echo ""
# echo "Make sure to add openAI or Gemini API key in ~/.ait.yml "
# echo ""
# echo "To start the assistant, run:"
# echo "  ./ait.py chat"
# echo "-------------------------------------------"


#!/bin/bash

# ---------------------------------------------
# AI Terminal Assistant Installer (Final Clean)
# Moves project to ~/abhi_ai and sets it up
# ---------------------------------------------

set -e

echo "[*] Preparing directories..."

# Define paths
SRC_DIR="$(pwd)"
TARGET_DIR="$HOME/abhi_ai"
VENV_DIR="$HOME/.abhi_ai"
BIN_PATH="/usr/local/bin/ait"

# Move current folder to ~/abhi_ai if not already there
if [ "$SRC_DIR" != "$TARGET_DIR" ]; then
    echo "[+] Moving project to $TARGET_DIR..."
    mv "$SRC_DIR" "$TARGET_DIR"
else
    echo "[✓] Already in $TARGET_DIR"
fi

cd "$TARGET_DIR"

echo "[+] Creating Python venv at $VENV_DIR..."
python3 -m venv "$VENV_DIR"

echo "[+] Activating venv..."
source "$VENV_DIR/bin/activate"

echo "[+] Upgrading pip..."
pip install --upgrade pip

echo "[+] Installing dependencies..."
pip install -r requirements.txt

# Create global launcher
echo "[+] Creating launcher at $BIN_PATH..."
sudo tee "$BIN_PATH" > /dev/null <<EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python3 "$TARGET_DIR/ait.py" "\$@"
EOF

sudo chmod +x "$BIN_PATH"

# Done
echo ""
echo "[✔] AI Terminal Assistant Installed!"
echo "-------------------------------------------"
echo "Venv: $VENV_DIR"
echo "Project: $TARGET_DIR"
echo "Run: ait chat"
echo "API Keys: ~/.ait.yml"
echo "-------------------------------------------"

#!/bin/bash

# -------------------------------------------------------
# AI Terminal Assistant Installer (by Abhi Singh)
# Installs AI Terminal Assistant and sets up everything you need.
# installs dependencies, and creates a global launcher.
# -------------------------------------------------------
echo "AI Terminal Assistant Installer (by Abhi Singh)"
set -e

# --------------------------------------
# Define key paths
# --------------------------------------
SRC_DIR="$(pwd)"
TARGET_DIR="$HOME/abhi_ai"
VENV_DIR="$HOME/.abhi_ai"
BIN_PATH="/usr/local/bin/ait"

# --------------------------------------
# Check Python
# --------------------------------------
if ! command -v python3 &>/dev/null; then
  echo "[!] Python3 not found. Please install it first."
  exit 1
fi

echo "[*] Preparing setup for AI Terminal Assistant..."

# --------------------------------------
# Move current folder to ~/abhi_ai
# --------------------------------------
if [ "$SRC_DIR" != "$TARGET_DIR" ]; then
  echo "[*] Moving project to: $TARGET_DIR ..."
  mv "$SRC_DIR" "$TARGET_DIR" || { echo "[!] Move failed. Check permissions."; exit 1; }
else
  echo "[✓] Project is already in: $TARGET_DIR"
fi

cd "$TARGET_DIR"

# --------------------------------------
# Create virtual environment
# --------------------------------------
echo "[*] Creating Python virtual environment at: $VENV_DIR ..."
python3 -m venv "$VENV_DIR" || { echo "[!] Failed to create virtualenv."; exit 1; }

echo "[*] Activating virtual environment..."
source "$VENV_DIR/bin/activate" || { echo "[!] Failed to activate virtualenv."; exit 1; }

# --------------------------------------
# Install dependencies
# --------------------------------------
echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing dependencies from requirements.txt..."
pip install -r requirements.txt || { echo "[!] pip install failed."; deactivate; exit 1; }

# --------------------------------------
# Create global launcher script
# --------------------------------------
echo "[*] Creating CLI launcher at: $BIN_PATH ..."
sudo tee "$BIN_PATH" > /dev/null <<EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python3 "$TARGET_DIR/ait.py" "\$@"
EOF

sudo chmod +x "$BIN_PATH"

# --------------------------------------
# Done!
# --------------------------------------
echo ""
echo "[✔] AI Terminal Assistant Installed Successfully!"
echo "-------------------------------------------"
echo ""
echo "To start the assistant from anywhere, type:"
echo "  ait chat"
echo ""
echo "Make sure to add your OpenAI or Gemini API key in:"
echo "  ~/.ait.yml"
echo "-------------------------------------------"
echo " → Facing errors or issues? Visit:"
echo " → GitHub: https://github.com/anodeus/ai_terminal_assistant"


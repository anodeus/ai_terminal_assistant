import os
import shutil
import subprocess
import tempfile
import zipfile
import urllib.request

GITHUB_ZIP_URL = "https://github.com/anodeus/ai_terminal_assistant/archive/refs/heads/master.zip"
INSTALL_DIR = os.path.expanduser("~/abhi_ai")
VENV_DIR = os.path.expanduser("~/.abhi_ai")
PIP_PATH = os.path.join(VENV_DIR, "bin", "pip")

def run_update():
    print("✓ Checking new version availability...")

    try:
        req = urllib.request.Request(GITHUB_ZIP_URL, method="HEAD")
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print("x New version not available (status:", response.status, ")")
                return
    except Exception as e:
        print("x Failed to reach server:", e)
        return

    print("✓ Starting update")

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "repo.zip")

        print("✓ Downloading latest version...")
        try:
            subprocess.run(["curl", "-L", GITHUB_ZIP_URL, "-o", zip_path], check=True)
        except subprocess.CalledProcessError:
            print("x Download failed. Check your internet. Try again!")
            return

        print("✓ Reading files...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmp)
        except zipfile.BadZipFile:
            print("x Invalid or corrupted file. Try again!")
            return

        new_code = os.path.join(tmp, "ai_terminal_assistant-master")

        confirm = input("\n[!] New version is ready. Do you want to install it? [y/N]: ").strip().lower()
        if confirm != "y":
            print("! Update cancelled. Keeping existing version.")
            return

        print("✓ Installing latest version...")
        for item in os.listdir(new_code):
            s = os.path.join(new_code, item)
            d = os.path.join(INSTALL_DIR, item)

            if os.path.abspath(s) == os.path.abspath(__file__):
                continue

            try:
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            except Exception as e:
                print(f"x Verifying failed. Try again! '{item}': {e}")
                return

        print("✓ Verifying files...")
        req_file = os.path.join(INSTALL_DIR, "requirements.txt")
        if os.path.exists(PIP_PATH) and os.path.exists(req_file):
            subprocess.run([PIP_PATH, "install", "-r", req_file])
        else:
            print("x Cannot find pip or requirements.txt.")

        print("\n✓ Update complete. You can now run 'ait chat'.")

if __name__ == "__main__":
    run_update()

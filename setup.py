"""One-command setup + launcher for tmdb-cli.

Usage:  python setup.py

First run : creates a .venv, installs dependencies, asks for your TMDB API
            key, saves it to .env, then starts the app ("Enter movie name:").
Later runs: skips straight to the app (re-asks for a key only if the saved
            one is missing or invalid).
"""
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
REQUIREMENTS = ROOT / "requirements.txt"
BASE_URL = "https://api.themoviedb.org/3"
VENV_DIR = ROOT / ".venv"


def ensure_venv():
    """Re-run this script inside ROOT/.venv (creating it first if needed)."""
    if sys.prefix != sys.base_prefix:  # already inside a venv
        return
    exe = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    py = VENV_DIR / exe
    if not py.exists():
        print("🐍 Creating virtual environment (.venv)...")
        try:
            venv.create(VENV_DIR, with_pip=True)
        except Exception:
            shutil.rmtree(VENV_DIR, ignore_errors=True)
            print(
                "❌ Couldn't create a venv. On Ubuntu/Debian run:\n"
                "     sudo apt install python3-venv"
            )
            sys.exit(1)
    sys.exit(subprocess.call([str(py), str(Path(__file__).resolve()), *sys.argv[1:]]))


def install_dependencies():
    """Install requirements.txt, but only if something is missing."""
    try:
        import dotenv  # noqa: F401
        import requests  # noqa: F401
        import rich  # noqa: F401
        return
    except ImportError:
        pass

    print("📦 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(REQUIREMENTS)]
        )
    except subprocess.CalledProcessError:
        print(
            "\n❌ Dependency install failed.\n"
            "   Check your internet connection and run: python3 setup.py"
        )
        sys.exit(1)


def check_key(key):
    """Return True if TMDB accepts the key, False if it rejects it."""
    import requests

    try:
        response = requests.get(
            f"{BASE_URL}/configuration", params={"api_key": key}, timeout=10
        )
    except requests.RequestException:
        print("❌ Couldn't reach TMDB. Check your internet connection and retry.")
        sys.exit(1)

    if response.status_code == 401:
        return False
    if response.status_code != 200:
        print(f"❌ TMDB returned HTTP {response.status_code}. Try again later.")
        sys.exit(1)
    return True


def ensure_api_key():
    """Make sure .env holds a valid key; ask for one if not."""
    from dotenv import dotenv_values

    saved = dotenv_values(ENV_FILE).get("TMDB_API_KEY") if ENV_FILE.exists() else None

    if saved:
        if check_key(saved):
            return
        print("⚠️  The saved TMDB API key was rejected. Let's replace it.")
    else:
        print("🔑 First-time setup: you need a free TMDB API key.")
        print("   Get one at https://www.themoviedb.org/settings/api (v3 'API Key').")

    while True:
        key = input("\nPaste your TMDB API key: ").strip()
        if not key:
            continue
        if check_key(key):
            break
        print("❌ TMDB rejected that key. Check it and try again.")

    ENV_FILE.write_text(f"TMDB_API_KEY={key}\n")
    print("✅ Key verified and saved to .env")


def main():
    ensure_venv()
    install_dependencies()
    ensure_api_key()
    # Run the app in a fresh process so it picks up the new .env
    sys.exit(subprocess.call([sys.executable, str(ROOT / "main.py")]))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Setup cancelled.")
        sys.exit(0)

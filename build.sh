#!/usr/bin/env bash
set -e

TARGET="${1:-linux}"
TARGET=$(echo "$TARGET" | tr '[:upper:]' '[:lower:]')

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Building Text-to-Speech for target: $TARGET ==="

# Use a local virtual environment (system Python is externally managed)
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

ICON_FLAG=""
if [ -f "tts.ico" ]; then
    ICON_FLAG="--icon=tts.ico --add-data=tts.ico:."
fi

case "$TARGET" in
    linux)
        echo "Building Linux executable..."
        pyinstaller --noconfirm --onefile --windowed --name "TextToSpeech" $ICON_FLAG tts.py
        echo "Build complete: dist/TextToSpeech"
        ;;
    windows)
        echo "Building Windows executable..."
        if command -v wine &> /dev/null; then
            wine pyinstaller --noconfirm --onefile --windowed --name "TextToSpeech" --icon=tts.ico --add-data="tts.ico;." tts.py
            echo "Build complete via Wine: dist/TextToSpeech.exe"
        else
            pyinstaller --noconfirm --onefile --windowed --name "TextToSpeech.exe" $ICON_FLAG tts.py
            echo "Build finished: dist/TextToSpeech.exe"
        fi
        ;;
    *)
        echo "Unknown target: $TARGET. Allowed: linux, windows"
        exit 1
        ;;
esac

# Text-to-Speech-by-Rajan

A modern desktop application built with Python and Tkinter for converting written text into spoken audio and exporting to audio files (MP3 / WAV).

## Features

- **Modern Dark UI:** Clean dark matte layout with responsive typography.
- **Non-Blocking Playback:** Asynchronous threaded audio synthesis keeps UI responsive.
- **Voice Selection:** Dynamic discovery and selection of installed system voices.
- **Speed & Volume Controls:** Customizable rate presets (Slow, Normal, Fast, Very Fast) and volume slider.
- **Audio Export:** Export speech to audio files with automatic safe filename formatting.
- **Cross-Platform Builds:** Ready-to-use build scripts for Linux and Windows executables via PyInstaller.

## Project Structure

```text
Text-to-Speech-by-Rajan/
├── tts.ico            # Application icon
├── tts.py             # Main entry point launcher
├── build.sh           # Linux/Bash build script
├── build.ps1          # Windows/PowerShell build script
└── src/
    ├── __init__.py    # Exports
    ├── config.py      # App constants, presets, theme palette
    ├── engine.py      # TTS audio engine & export processing
    ├── ui.py          # Tkinter interface & controls
    └── utils.py       # Resource path resolution helper
```

## Running Locally

Requires Python 3.8+ and dependencies:

```bash
pip install pyttsx3
# On Linux, espeak and ffmpeg may also be required:
# sudo apt-get install espeak ffmpeg
python tts.py
```

## Building Executables

### Linux (Bash)
```bash
chmod +x build.sh
./build.sh linux
```
Output: `dist/TextToSpeech`

### Windows (PowerShell)
```powershell
.\build.ps1 -Target windows
```
Output: `dist/TextToSpeech.exe`

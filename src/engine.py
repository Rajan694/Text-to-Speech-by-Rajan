import pyttsx3
import threading
import re
import os

class TTSEngine:
    def __init__(self):
        self._is_busy = False
        self._lock = threading.Lock()
        self.voices = []
        self._load_voices()

    def _load_voices(self):
        try:
            temp_eng = pyttsx3.init()
            self.voices = temp_eng.getProperty("voices") or []
        except Exception:
            self.voices = []

    def get_voice_names(self) -> list[str]:
        if not self.voices:
            return ["Default Voice"]
        names = []
        for i, v in enumerate(self.voices):
            name = getattr(v, "name", f"Voice {i + 1}")
            names.append(f"{i + 1}. {name}")
        return names

    def speak(self, text: str, voice_index: int, rate: int, volume: float, on_finish=None, on_error=None):
        def _worker():
            with self._lock:
                self._is_busy = True
                try:
                    eng = pyttsx3.init()
                    eng.setProperty("rate", rate)
                    eng.setProperty("volume", max(0.0, min(1.0, volume)))
                    
                    if 0 <= voice_index < len(self.voices):
                        eng.setProperty("voice", self.voices[voice_index].id)

                    eng.say(text)
                    eng.runAndWait()
                except Exception as e:
                    if on_error:
                        on_error(str(e))
                finally:
                    self._is_busy = False
                    if on_finish:
                        on_finish()

        threading.Thread(target=_worker, daemon=True).start()

    def save_audio(self, text: str, output_path: str, voice_index: int, rate: int, volume: float, on_finish=None, on_error=None):
        def _worker():
            with self._lock:
                self._is_busy = True
                try:
                    eng = pyttsx3.init()
                    eng.setProperty("rate", rate)
                    eng.setProperty("volume", max(0.0, min(1.0, volume)))

                    if 0 <= voice_index < len(self.voices):
                        eng.setProperty("voice", self.voices[voice_index].id)

                    eng.save_to_file(text, output_path)
                    eng.runAndWait()
                    if on_finish:
                        on_finish(output_path)
                except Exception as e:
                    if on_error:
                        on_error(str(e))
                finally:
                    self._is_busy = False

        threading.Thread(target=_worker, daemon=True).start()

    def sanitize_filename(self, text: str) -> str:
        snippet = text.strip().split("\n")[0][:25]
        clean = re.sub(r'[\\/*?:"<>|]', "", snippet).strip()
        return clean if clean else "speech_output"

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from . import config
from .engine import TTSEngine
from .utils import resource_path

class TTSApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = TTSEngine()

        self._setup_window()
        self._create_header()
        self._create_text_input()
        self._create_settings_card()
        self._create_action_buttons()
        self._create_status_bar()

    def _setup_window(self):
        self.root.title(config.APP_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(500, 560)
        self.root.configure(bg=config.BG_MAIN)

        icon_path = resource_path(config.ICON_FILE)
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    def _create_header(self):
        header = tk.Frame(self.root, bg=config.BG_MAIN)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="Text to Speech Studio",
            font=config.TITLE_FONT,
            bg=config.BG_MAIN,
            fg=config.FG_MAIN
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Convert text to natural speech audio and export to MP3/WAV",
            font=config.SUBTITLE_FONT,
            bg=config.BG_MAIN,
            fg=config.FG_MUTED
        ).pack(anchor="w")

    def _create_text_input(self):
        frame = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        frame.pack(fill="both", expand=True, padx=20, pady=6)

        self.text_area = tk.Text(
            frame,
            font=config.TEXT_FONT,
            bg=config.BG_INPUT,
            fg=config.FG_MAIN,
            insertbackground=config.FG_MAIN,
            relief="flat",
            bd=0,
            padx=12,
            pady=12,
            wrap="word"
        )
        self.text_area.pack(fill="both", expand=True)

        self.info_lbl = tk.Label(
            frame,
            text="0 characters | 0 words",
            font=(config.FONT_FAMILY, 9),
            bg=config.BG_INPUT,
            fg=config.FG_MUTED,
            anchor="e",
            padx=10,
            pady=4
        )
        self.info_lbl.pack(fill="x")
        self.text_area.bind("<KeyRelease>", self._update_counts)

    def _update_counts(self, event=None):
        content = self.text_area.get("1.0", "end-1c")
        chars = len(content)
        words = len(content.split()) if content.strip() else 0
        self.info_lbl.config(text=f"{chars} characters | {words} words")

    def _create_settings_card(self):
        card = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        card.pack(fill="x", padx=20, pady=6)

        inner = tk.Frame(card, bg=config.BG_CARD, padx=12, pady=10)
        inner.pack(fill="x")

        # Voice Selector
        v_frame = tk.Frame(inner, bg=config.BG_CARD)
        v_frame.pack(fill="x", pady=2)

        tk.Label(
            v_frame,
            text="Voice:",
            font=config.LABEL_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            width=8,
            anchor="w"
        ).pack(side="left")

        voices = self.engine.get_voice_names()
        self.voice_combo = ttk.Combobox(v_frame, values=voices, state="readonly")
        if voices:
            self.voice_combo.current(0)
        self.voice_combo.pack(side="left", fill="x", expand=True)

        # Speed Selector
        s_frame = tk.Frame(inner, bg=config.BG_CARD)
        s_frame.pack(fill="x", pady=4)

        tk.Label(
            s_frame,
            text="Speed:",
            font=config.LABEL_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            width=8,
            anchor="w"
        ).pack(side="left")

        self.speed_var = tk.StringVar(value="Normal")
        self.speed_combo = ttk.Combobox(
            s_frame,
            textvariable=self.speed_var,
            values=list(config.SPEED_RATES.keys()),
            state="readonly",
            width=12
        )
        self.speed_combo.pack(side="left")

        # Volume slider
        tk.Label(
            s_frame,
            text="Volume:",
            font=config.LABEL_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            padx=10
        ).pack(side="left")

        self.volume_scale = tk.Scale(
            s_frame,
            from_=0,
            to=100,
            orient="horizontal",
            bg=config.BG_CARD,
            fg=config.FG_MAIN,
            highlightthickness=0,
            troughcolor=config.BG_INPUT,
            bd=0,
            length=120
        )
        self.volume_scale.set(100)
        self.volume_scale.pack(side="left", fill="x", expand=True)

    def _create_action_buttons(self):
        btn_frame = tk.Frame(self.root, bg=config.BG_MAIN)
        btn_frame.pack(fill="x", padx=20, pady=8)

        self.play_btn = tk.Button(
            btn_frame,
            text="▶ Play Speech",
            command=self._speak,
            font=config.BUTTON_FONT,
            bg=config.ACCENT_PLAY,
            fg="#FFFFFF",
            activebackground=config.ACCENT_PLAY_HOVER,
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2"
        )
        self.play_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.save_btn = tk.Button(
            btn_frame,
            text="💾 Save to Audio",
            command=self._save_audio,
            font=config.BUTTON_FONT,
            bg=config.ACCENT_SAVE,
            fg="#FFFFFF",
            activebackground=config.ACCENT_SAVE_HOVER,
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2"
        )
        self.save_btn.pack(side="right", fill="x", expand=True, padx=(6, 0))

    def _create_status_bar(self):
        status_card = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        status_card.pack(fill="x", padx=20, pady=(2, 14))

        self.status_lbl = tk.Label(
            status_card,
            text="Ready.",
            font=config.STATUS_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            anchor="w",
            padx=12,
            pady=6
        )
        self.status_lbl.pack(fill="x")

    def _get_params(self):
        text = self.text_area.get("1.0", "end-1c").strip()
        voice_idx = self.voice_combo.current() if self.voice_combo.current() >= 0 else 0
        speed_key = self.speed_var.get()
        rate = config.SPEED_RATES.get(speed_key, 160)
        volume = self.volume_scale.get() / 100.0
        return text, voice_idx, rate, volume

    def _set_busy_state(self, is_busy: bool, message: str):
        state = "disabled" if is_busy else "normal"
        self.play_btn.config(state=state)
        self.save_btn.config(state=state)
        self.status_lbl.config(
            text=message,
            fg=config.ACCENT_PLAY_HOVER if is_busy else config.FG_MUTED
        )

    def _speak(self):
        text, voice_idx, rate, volume = self._get_params()
        if not text:
            messagebox.showwarning("Empty Text", "Please enter some text to speak.")
            return

        self._set_busy_state(True, "Speaking...")

        def on_finish():
            self.root.after(0, lambda: self._set_busy_state(False, "Ready."))

        def on_error(err):
            self.root.after(0, lambda: messagebox.showerror("Playback Error", err))
            self.root.after(0, lambda: self._set_busy_state(False, "Error occurred."))

        self.engine.speak(text, voice_idx, rate, volume, on_finish, on_error)

    def _save_audio(self):
        text, voice_idx, rate, volume = self._get_params()
        if not text:
            messagebox.showwarning("Empty Text", "Please enter text to export.")
            return

        default_name = self.engine.sanitize_filename(text)
        filepath = filedialog.asksaveasfilename(
            initialfile=f"{default_name}.mp3",
            defaultextension=".mp3",
            filetypes=[("MP3 Audio (*.mp3)", "*.mp3"), ("WAV Audio (*.wav)", "*.wav"), ("All Files (*.*)", "*.*")]
        )
        if not filepath:
            return

        self._set_busy_state(True, "Exporting audio file...")

        def on_finish(saved_path):
            self.root.after(0, lambda: self._set_busy_state(False, f"Saved audio: {os.path.basename(saved_path)}"))
            self.root.after(0, lambda: messagebox.showinfo("Saved", f"Audio successfully saved to:\n{saved_path}"))

        def on_error(err):
            self.root.after(0, lambda: messagebox.showerror("Export Error", err))
            self.root.after(0, lambda: self._set_busy_state(False, "Export failed."))

        self.engine.save_audio(text, filepath, voice_idx, rate, volume, on_finish, on_error)

"""Sound playback for Pomodoro timer — built-in + MP3 via Windows MCI."""

import os
import winsound
import ctypes
from glob import glob

# ── Sound options ─────────────────────────────────────

BUILTIN_KEYS = ["none", "beep", "beep_done", "bell", "chime"]
BUILTIN_LABELS_EN = ["🔇 Silent", "🔔 Beep", "🔔↑ Done!", "🔔 Bell", "🎵 Chime"]
BUILTIN_LABELS_ZH = ["🔇 静音", "🔔 蜂鸣", "🔔↑ 完成！", "🔔 铃声", "🎵 叮咚"]


def _discover_mp3s():
    """Find all .mp3/.wav files in the app directory and return (key, display-name) pairs."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    found = []
    for ext in ("*.mp3", "*.wav"):
        for fp in sorted(glob(os.path.join(app_dir, ext))):
            name = os.path.splitext(os.path.basename(fp))[0]
            key = f"__file__{fp}"
            display = f"🎵 {name}"
            found.append((key, display))
    return found


MP3_FILES = _discover_mp3s()
# Order: none → MP3s → built-in beeps
SOUND_CHOICES = ["none"] + [k for k, _ in MP3_FILES] + BUILTIN_KEYS[1:]
SOUND_LABELS_EN = (["🔇 Silent"]
                   + [d for _, d in MP3_FILES]
                   + BUILTIN_LABELS_EN[1:])
SOUND_LABELS_ZH = (["🔇 静音"]
                   + [d for _, d in MP3_FILES]
                   + BUILTIN_LABELS_ZH[1:])


# ── MCI playback (handles MP3 on Windows with no extra deps) ──

_mci_open = ctypes.windll.winmm.mciSendStringW
_mci_err_buf = ctypes.create_unicode_buffer(256)


def _mci_close():
    """Close any previously opened MCI device. Always safe to call."""
    try:
        _mci_open("close sound", _mci_err_buf, 256, 0)
    except Exception:
        pass


def _play_mp3(path: str):
    """Play an MP3 (or WAV) via Windows MCI — async, non-blocking."""
    if not os.path.exists(path):
        return _error_beep()
    try:
        # Normalise path for MCI (needs double backslashes)
        safe = path.replace("\\", "\\\\")
        _mci_close()
        rc = _mci_open(
            f'open "{safe}" type mpegvideo alias sound',
            _mci_err_buf, 256, 0,
        )
        if rc != 0:
            # fallback: try as waveaudio
            rc = _mci_open(
                f'open "{safe}" type waveaudio alias sound',
                _mci_err_buf, 256, 0,
            )
            if rc != 0:
                _mci_close()
                # Last attempt: just play as default
                rc = _mci_open(
                    f'open "{safe}" alias sound',
                    _mci_err_buf, 256, 0,
                )
                if rc != 0:
                    return _error_beep()
        _mci_open("play sound", None, 0, 0)
    except Exception:
        _error_beep()


def _stop_mci():
    """Stop and close any currently playing MCI sound."""
    try:
        _mci_open("close sound", _mci_err_buf, 256, 0)
    except Exception:
        pass


# ── Built-in sounds ───────────────────────────────────


def _play_beep():
    winsound.Beep(880, 500)


def _play_beep_done():
    winsound.Beep(660, 200)
    winsound.Beep(880, 300)


def _play_bell():
    winsound.Beep(440, 400)


def _play_chime():
    winsound.Beep(523, 150)
    winsound.Beep(659, 150)
    winsound.Beep(784, 250)


def _error_beep():
    winsound.Beep(200, 500)


def _play_file(path: str):
    """Play a .wav file via winsound (for WAV-only mode)."""
    try:
        _stop_mci()
        winsound.PlaySound(path, winsound.SND_ASYNC)
    except Exception:
        _error_beep()


# ── Public API ────────────────────────────────────────


def play_sound(key: str):
    """Play a sound by key. Built-in keys or '__file__<path>' for custom files."""
    key = (key or "none").strip()
    if key == "none":
        return

    # Built-in sounds
    if key == "beep":
        _play_beep()
    elif key == "beep_done":
        _play_beep_done()
    elif key == "bell":
        _play_bell()
    elif key == "chime":
        _play_chime()

    # Custom file (__file__<path> format)
    elif key.startswith("__file__"):
        fp = key[len("__file__"):]
        ext = os.path.splitext(fp)[1].lower()
        if ext == ".wav":
            _play_file(fp)
        else:
            _play_mp3(fp)

    # Raw path (legacy)
    elif os.path.sep in key or key.startswith("__file__"):
        ext = os.path.splitext(key)[1].lower()
        if ext == ".wav":
            _play_file(key)
        else:
            _play_mp3(key)

    # Unknown built-in key — try as raw file path
    else:
        _play_file(key)

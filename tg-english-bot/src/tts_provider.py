"""Generates a short pronunciation audio clip via gTTS (Google Text-to-Speech)."""
import tempfile
from pathlib import Path
from typing import Optional
from . import config


def synthesize(text: str) -> Optional[Path]:
    if not config.ENABLE_AUDIO:
        return None
    try:
        from gtts import gTTS
    except ImportError:
        return None
    try:
        tmp_dir = Path(tempfile.mkdtemp())
        out_path = tmp_dir / "pronunciation.mp3"
        kwargs = {"text": text, "lang": "en", "slow": False}
        if config.PROXIES:
            kwargs["proxies"] = config.PROXIES  # supported in gTTS >= 2.3
        gTTS(**kwargs).save(str(out_path))
        return out_path
    except Exception:
        return None

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
VOCAB_PATH = DATA_DIR / "vocabulary.json"
STATE_PATH = DATA_DIR / "state.json"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

# Optional HTTP(S)/SOCKS proxy, e.g. http://user:pass@host:port or
# socks5://host:port. Needed if Telegram/Unsplash/Google TTS are blocked
# from the network where the script runs. Leave empty to disable.
PROXY_URL = os.getenv("PROXY_URL", "").strip()
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None

ENABLE_IMAGES = os.getenv("ENABLE_IMAGES", "true").lower() == "true" and bool(UNSPLASH_ACCESS_KEY)
ENABLE_AUDIO = os.getenv("ENABLE_AUDIO", "true").lower() == "true"

# Order in which CEFR levels are introduced.
LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Leitner boxes: box index -> how many runs (script executions) must pass
# before the word is due for review again. With a run every 30 minutes,
# these roughly correspond to ~30min / ~1.5h / ~3.5h / ~8h / ~17.5h.
BOX_INTERVALS_IN_RUNS = [1, 3, 7, 16, 35]
MAX_BOX = len(BOX_INTERVALS_IN_RUNS) - 1

"""Thin wrapper around the Telegram Bot API for sending lesson messages."""
import requests
from . import config

API_BASE = "https://api.telegram.org/bot{token}"


def _url(method: str) -> str:
    return f"{API_BASE.format(token=config.BOT_TOKEN)}/{method}"


def send_text(text: str, parse_mode: str = "HTML"):
    resp = requests.post(
        _url("sendMessage"),
        data={"chat_id": config.CHAT_ID, "text": text, "parse_mode": parse_mode},
        proxies=config.PROXIES,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def send_photo(image_url: str, caption: str, parse_mode: str = "HTML"):
    resp = requests.post(
        _url("sendPhoto"),
        data={
            "chat_id": config.CHAT_ID,
            "photo": image_url,
            "caption": caption,
            "parse_mode": parse_mode,
        },
        proxies=config.PROXIES,
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def send_voice(file_path):
    with open(file_path, "rb") as f:
        resp = requests.post(
            _url("sendVoice"),
            data={"chat_id": config.CHAT_ID},
            files={"voice": f},
            proxies=config.PROXIES,
            timeout=30,
        )
    resp.raise_for_status()
    return resp.json()

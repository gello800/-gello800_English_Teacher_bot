"""Entry point: pick the next card and send it to Telegram.

Run with: python -m src.main
"""
import sys

from . import config
from .vocabulary import load_vocabulary, index_by_id
from .state_manager import load_state, save_state
from .scheduler_logic import pick_card
from .message_format import build_caption
from .image_provider import get_image_url
from .tts_provider import synthesize
from . import telegram_client


def main():
    if not config.BOT_TOKEN or not config.CHAT_ID:
        print("BOT_TOKEN / CHAT_ID are not set. Fill in .env or repo secrets.", file=sys.stderr)
        sys.exit(1)

    by_level = load_vocabulary()
    flat_index = index_by_id(by_level)
    state = load_state()

    entry, is_review = pick_card(state, by_level, flat_index)

    if entry is None:
        print("Vocabulary is empty — nothing to send.")
        save_state(state)
        return

    times_reviewed = state["cards"][entry["id"]]["times_reviewed"]
    caption = build_caption(entry, is_review, times_reviewed)

    image_url = get_image_url(entry["en"]) if config.ENABLE_IMAGES else None
    if image_url:
        telegram_client.send_photo(image_url, caption)
    else:
        telegram_client.send_text(caption)

    audio_path = synthesize(entry["en"]) if config.ENABLE_AUDIO else None
    if audio_path:
        telegram_client.send_voice(audio_path)

    save_state(state)
    print(f"Sent '{entry['en']}' ({entry['level']}, review={is_review}).")


if __name__ == "__main__":
    main()

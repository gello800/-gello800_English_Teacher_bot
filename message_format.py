"""Builds the HTML-formatted Telegram message for a card."""

LEVEL_EMOJI = {
    "A1": "🟢", "A2": "🟢", "B1": "🔵", "B2": "🔵", "C1": "🟣", "C2": "🟣",
}


def build_caption(entry: dict, is_review: bool, times_reviewed: int) -> str:
    kind = "Фраза" if entry.get("type") == "phrase" else "Слово"
    tag = f"🔁 Повторение №{times_reviewed}" if is_review else f"✨ Новое {kind.lower()}"
    emoji = LEVEL_EMOJI.get(entry.get("level"), "📘")

    lines = [
        f"{emoji} Уровень {entry.get('level', '?')} · {tag}",
        "",
        f"<b>{entry['en']}</b> {entry.get('ipa', '')}".strip(),
        entry["ru"],
    ]

    if entry.get("example_en"):
        lines += ["", f"📝 <i>{entry['example_en']}</i>"]
        if entry.get("example_ru"):
            lines.append(entry["example_ru"])

    return "\n".join(lines)

"""Loads and indexes the vocabulary bank."""
import json
from . import config


def load_vocabulary():
    """Returns a dict: level -> list[entry], preserving file order within a level."""
    with open(config.VOCAB_PATH, encoding="utf-8") as f:
        entries = json.load(f)

    by_level = {level: [] for level in config.LEVEL_ORDER}
    for entry in entries:
        level = entry.get("level")
        if level not in by_level:
            # Unknown level in the data file — keep it, just append to the order.
            by_level[level] = []
            config.LEVEL_ORDER.append(level)
        by_level[level].append(entry)

    return by_level


def index_by_id(by_level):
    flat = {}
    for entries in by_level.values():
        for entry in entries:
            flat[entry["id"]] = entry
    return flat

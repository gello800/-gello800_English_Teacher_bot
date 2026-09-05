"""Reads and writes the bot's progress state (data/state.json)."""
import json
from . import config

DEFAULT_STATE = {
    "run_count": 0,
    "current_level_index": 0,
    "sent_ids_in_level": [],
    "cards": {},
    # cards[word_id] = {
    #   "box": int,               # Leitner box, 0..MAX_BOX
    #   "next_due_run": int,      # run_count at which this card should be shown again
    #   "times_reviewed": int,
    # }
}


def load_state():
    if not config.STATE_PATH.exists():
        return json.loads(json.dumps(DEFAULT_STATE))
    with open(config.STATE_PATH, encoding="utf-8") as f:
        state = json.load(f)
    # Backfill any keys missing from an older state file.
    for key, value in DEFAULT_STATE.items():
        state.setdefault(key, value)
    return state


def save_state(state):
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

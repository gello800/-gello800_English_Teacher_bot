"""Decides which card (word/phrase) to send on this run.

Priority each run:
  1. A card that is due for review (Leitner box schedule) -> send as review,
     bump its box up (spaced repetition strengthens what's already known).
  2. Otherwise, the next unseen word of the current CEFR level -> send as new.
  3. If the current level has no unseen words left, advance to the next level
     and pick its first word.
"""
from . import config


def _due_review_id(state):
    due = [
        (card["next_due_run"], word_id)
        for word_id, card in state["cards"].items()
        if card["next_due_run"] <= state["run_count"]
    ]
    if not due:
        return None
    # Most overdue first.
    due.sort(key=lambda pair: pair[0])
    return due[0][1]


def _advance_level_if_needed(state, by_level):
    while state["current_level_index"] < len(config.LEVEL_ORDER) - 1:
        level = config.LEVEL_ORDER[state["current_level_index"]]
        level_ids = {e["id"] for e in by_level.get(level, [])}
        if level_ids and level_ids.issubset(set(state["sent_ids_in_level"])):
            state["current_level_index"] += 1
            state["sent_ids_in_level"] = []
        else:
            break


def _next_new_id(state, by_level):
    _advance_level_if_needed(state, by_level)
    level = config.LEVEL_ORDER[state["current_level_index"]]
    entries = by_level.get(level, [])
    for entry in entries:
        if entry["id"] not in state["sent_ids_in_level"]:
            return entry["id"], level
    return None, level


def pick_card(state, by_level, flat_index):
    """Returns (entry_dict, is_review: bool). Mutates state in place."""
    state["run_count"] += 1

    review_id = _due_review_id(state)
    if review_id and review_id in flat_index:
        card = state["cards"][review_id]
        card["box"] = min(card["box"] + 1, config.MAX_BOX)
        card["times_reviewed"] += 1
        card["next_due_run"] = state["run_count"] + config.BOX_INTERVALS_IN_RUNS[card["box"]]
        return flat_index[review_id], True

    new_id, level = _next_new_id(state, by_level)
    if new_id is None:
        # Whole vocabulary exhausted: fall back to reviewing the least-recently
        # reinforced known card so the bot never goes silent.
        if state["cards"]:
            oldest_id = min(state["cards"], key=lambda w: state["cards"][w]["next_due_run"])
            card = state["cards"][oldest_id]
            card["box"] = min(card["box"] + 1, config.MAX_BOX)
            card["times_reviewed"] += 1
            card["next_due_run"] = state["run_count"] + config.BOX_INTERVALS_IN_RUNS[card["box"]]
            return flat_index[oldest_id], True
        return None, False

    state["sent_ids_in_level"].append(new_id)
    state["cards"][new_id] = {
        "box": 0,
        "times_reviewed": 0,
        "next_due_run": state["run_count"] + config.BOX_INTERVALS_IN_RUNS[0],
    }
    return flat_index[new_id], False

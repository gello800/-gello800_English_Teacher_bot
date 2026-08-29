"""
Простой слой доступа к SQLite базе данных.
Хранит пользователей и их персональные словари.
"""
import sqlite3
from contextlib import contextmanager
from typing import List, Tuple, Optional

from config import DB_PATH


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                learned INTEGER DEFAULT 0,
                added_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, word),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
        )


def add_user(user_id: int, username: Optional[str]) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username),
        )


def add_word(user_id: int, word: str, translation: str) -> bool:
    """Возвращает True, если слово добавлено, False если уже существует."""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO words (user_id, word, translation) VALUES (?, ?, ?)",
                (user_id, word.strip().lower(), translation.strip()),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_words(user_id: int) -> List[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, word, translation, learned FROM words WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def delete_word(user_id: int, word_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM words WHERE id = ? AND user_id = ?", (word_id, user_id)
        )


def get_random_words(user_id: int, limit: int = 4) -> List[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT word, translation FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT ?",
            (user_id, limit),
        )
        return cur.fetchall()


def count_user_words(user_id: int) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT COUNT(*) as cnt FROM words WHERE user_id = ?", (user_id,)
        )
        return cur.fetchone()["cnt"]


def mark_learned(user_id: int, word: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE words SET learned = 1 WHERE user_id = ? AND word = ?",
            (user_id, word.strip().lower()),
        )

import sqlite3
from pathlib import Path

DB_PATH = Path("chat_history.db")

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)


def save_message(user, role, content):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO chat_messages (user, role, content) VALUES (?, ?, ?)",
            (user, role, content)
        )

def load_chat(user, limit=100):
    with get_conn() as conn:
        cursor = conn.execute(
            """
            SELECT role, content
            FROM chat_messages
            WHERE user = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (user, limit)
        )
        return [
            {"role": role, "content": content}
            for role, content in cursor.fetchall()
        ]

def clear_chat(user):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM chat_messages WHERE user = ?",
            (user,)
        )
from chat_db import get_conn


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

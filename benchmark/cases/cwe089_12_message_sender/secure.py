import sqlite3

def look_up_message_sender(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT message_text FROM messages WHERE sender = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


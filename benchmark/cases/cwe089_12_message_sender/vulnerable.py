import sqlite3

def look_up_message_sender(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT message_text FROM messages WHERE sender = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


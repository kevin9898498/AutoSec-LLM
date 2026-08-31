import sqlite3

def look_up_session_user(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT session_label FROM sessions WHERE user_id = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


import sqlite3

def look_up_user_profile(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT display_name FROM users WHERE username = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


import sqlite3

def look_up_user_profile(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT display_name FROM users WHERE username = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


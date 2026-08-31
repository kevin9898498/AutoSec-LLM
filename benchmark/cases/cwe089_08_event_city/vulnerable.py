import sqlite3

def look_up_event_city(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT event_name FROM events WHERE city = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


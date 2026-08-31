import sqlite3

def look_up_device_owner(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT device_name FROM devices WHERE owner = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


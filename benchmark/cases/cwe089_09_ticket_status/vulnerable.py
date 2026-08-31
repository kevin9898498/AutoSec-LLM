import sqlite3

def look_up_ticket_status(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT ticket_title FROM tickets WHERE status = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


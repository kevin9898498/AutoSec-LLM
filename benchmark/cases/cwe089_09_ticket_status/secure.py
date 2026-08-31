import sqlite3

def look_up_ticket_status(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT ticket_title FROM tickets WHERE status = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


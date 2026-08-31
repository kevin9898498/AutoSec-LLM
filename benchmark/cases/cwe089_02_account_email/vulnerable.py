import sqlite3

def look_up_account_email(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT account_id FROM accounts WHERE email = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


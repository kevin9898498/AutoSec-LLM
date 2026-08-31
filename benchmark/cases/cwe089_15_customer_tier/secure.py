import sqlite3

def look_up_customer_tier(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT customer_name FROM customers WHERE tier = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


import sqlite3

def look_up_order_customer(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT order_ref FROM orders WHERE customer_id = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


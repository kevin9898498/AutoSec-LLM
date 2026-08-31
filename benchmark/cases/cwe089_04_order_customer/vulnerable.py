import sqlite3

def look_up_order_customer(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT order_ref FROM orders WHERE customer_id = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


import sqlite3

def look_up_product_category(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT product_name FROM products WHERE category = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


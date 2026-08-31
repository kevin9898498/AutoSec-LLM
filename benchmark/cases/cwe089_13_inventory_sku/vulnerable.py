import sqlite3

def look_up_inventory_sku(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT item_name FROM inventory WHERE sku = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


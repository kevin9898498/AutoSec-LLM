import sqlite3

def look_up_inventory_sku(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT item_name FROM inventory WHERE sku = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


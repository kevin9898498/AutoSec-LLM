import sqlite3

def look_up_supplier_region(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT supplier_name FROM suppliers WHERE region = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


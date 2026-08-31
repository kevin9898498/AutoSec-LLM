import sqlite3

def look_up_invoice_client(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT invoice_ref FROM invoices WHERE client_id = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


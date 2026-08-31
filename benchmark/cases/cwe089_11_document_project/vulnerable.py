import sqlite3

def look_up_document_project(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT document_name FROM documents WHERE project = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


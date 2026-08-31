import sqlite3

def look_up_comment_author(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT comment_text FROM comments WHERE author = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


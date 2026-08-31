import sqlite3

def look_up_article_author(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT article_title FROM articles WHERE author = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


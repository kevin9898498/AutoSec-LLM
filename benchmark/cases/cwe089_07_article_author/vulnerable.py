import sqlite3

def look_up_article_author(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT article_title FROM articles WHERE author = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


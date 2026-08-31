import sqlite3


def authenticate_user(username: str, password: str) -> bool:
    conn = sqlite3.connect("users.db")
    query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
    return conn.execute(query).fetchone() is not None

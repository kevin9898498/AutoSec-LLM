import sqlite3

def look_up_employee_department(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT employee_name FROM employees WHERE department = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


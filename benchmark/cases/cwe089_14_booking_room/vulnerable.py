import sqlite3

def look_up_booking_room(conn: sqlite3.Connection, value: str) -> list[str]:
    query = f"SELECT reservation_code FROM bookings WHERE room = '{value}'"
    return [row[0] for row in conn.execute(query).fetchall()]


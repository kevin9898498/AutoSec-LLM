import sqlite3

def look_up_booking_room(conn: sqlite3.Connection, value: str) -> list[str]:
    query = "SELECT reservation_code FROM bookings WHERE room = ?"
    return [row[0] for row in conn.execute(query, (value,)).fetchall()]


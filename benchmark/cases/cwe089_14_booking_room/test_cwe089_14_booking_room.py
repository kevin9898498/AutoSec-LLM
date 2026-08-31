from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_14_booking_room", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_14_booking_room_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE bookings (room TEXT, reservation_code TEXT)")
    conn.executemany("INSERT INTO bookings (room, reservation_code) VALUES (?, ?)", [
        ("A101", "reserve-01"),
        ("B202", "reserve-02"),
    ])
    lookup = getattr(module, "look_up_booking_room")
    assert lookup(conn, "A101") == ["reserve-01"]
    assert lookup(conn, "' OR 1=1 --") == []


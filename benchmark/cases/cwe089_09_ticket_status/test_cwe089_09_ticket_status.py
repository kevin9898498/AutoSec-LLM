from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_09_ticket_status", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_09_ticket_status_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE tickets (status TEXT, ticket_title TEXT)")
    conn.executemany("INSERT INTO tickets (status, ticket_title) VALUES (?, ?)", [
        ("open", "Fix parser"),
        ("closed", "Update docs"),
    ])
    lookup = getattr(module, "look_up_ticket_status")
    assert lookup(conn, "open") == ["Fix parser"]
    assert lookup(conn, "' OR 1=1 --") == []


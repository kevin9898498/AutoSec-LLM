from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_12_message_sender", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_12_message_sender_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE messages (sender TEXT, message_text TEXT)")
    conn.executemany("INSERT INTO messages (sender, message_text) VALUES (?, ?)", [
        ("alice", "hello"),
        ("bob", "status update"),
    ])
    lookup = getattr(module, "look_up_message_sender")
    assert lookup(conn, "alice") == ["hello"]
    assert lookup(conn, "' OR 1=1 --") == []


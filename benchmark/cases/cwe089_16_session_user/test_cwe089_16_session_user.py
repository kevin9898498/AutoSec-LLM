from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_16_session_user", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_16_session_user_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE sessions (user_id TEXT, session_label TEXT)")
    conn.executemany("INSERT INTO sessions (user_id, session_label) VALUES (?, ?)", [
        ("user-a", "morning"),
        ("user-b", "afternoon"),
    ])
    lookup = getattr(module, "look_up_session_user")
    assert lookup(conn, "user-a") == ["morning"]
    assert lookup(conn, "' OR 1=1 --") == []


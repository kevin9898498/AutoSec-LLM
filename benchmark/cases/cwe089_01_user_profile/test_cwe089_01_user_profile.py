from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_01_user_profile", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_01_user_profile_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (username TEXT, display_name TEXT)")
    conn.executemany("INSERT INTO users (username, display_name) VALUES (?, ?)", [
        ("alice", "Alice"),
        ("bob", "Bob"),
    ])
    lookup = getattr(module, "look_up_user_profile")
    assert lookup(conn, "alice") == ["Alice"]
    assert lookup(conn, "' OR 1=1 --") == []


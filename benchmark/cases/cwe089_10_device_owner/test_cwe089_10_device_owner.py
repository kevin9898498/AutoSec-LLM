from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_10_device_owner", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_10_device_owner_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE devices (owner TEXT, device_name TEXT)")
    conn.executemany("INSERT INTO devices (owner, device_name) VALUES (?, ?)", [
        ("alice", "laptop-01"),
        ("bob", "phone-02"),
    ])
    lookup = getattr(module, "look_up_device_owner")
    assert lookup(conn, "alice") == ["laptop-01"]
    assert lookup(conn, "' OR 1=1 --") == []


from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_02_account_email", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_02_account_email_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (email TEXT, account_id TEXT)")
    conn.executemany("INSERT INTO accounts (email, account_id) VALUES (?, ?)", [
        ("alice@example.test", "acct-001"),
        ("bob@example.test", "acct-002"),
    ])
    lookup = getattr(module, "look_up_account_email")
    assert lookup(conn, "alice@example.test") == ["acct-001"]
    assert lookup(conn, "' OR 1=1 --") == []


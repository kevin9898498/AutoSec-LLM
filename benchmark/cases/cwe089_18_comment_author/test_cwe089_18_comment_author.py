from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_18_comment_author", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_18_comment_author_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE comments (author TEXT, comment_text TEXT)")
    conn.executemany("INSERT INTO comments (author, comment_text) VALUES (?, ?)", [
        ("alice", "looks good"),
        ("bob", "needs changes"),
    ])
    lookup = getattr(module, "look_up_comment_author")
    assert lookup(conn, "alice") == ["looks good"]
    assert lookup(conn, "' OR 1=1 --") == []


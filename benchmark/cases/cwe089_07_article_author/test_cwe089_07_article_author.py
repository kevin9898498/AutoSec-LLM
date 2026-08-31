from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_07_article_author", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_07_article_author_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE articles (author TEXT, article_title TEXT)")
    conn.executemany("INSERT INTO articles (author, article_title) VALUES (?, ?)", [
        ("Ada", "Secure Python"),
        ("Ben", "Testing Notes"),
    ])
    lookup = getattr(module, "look_up_article_author")
    assert lookup(conn, "Ada") == ["Secure Python"]
    assert lookup(conn, "' OR 1=1 --") == []


from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_11_document_project", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_11_document_project_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE documents (project TEXT, document_name TEXT)")
    conn.executemany("INSERT INTO documents (project, document_name) VALUES (?, ?)", [
        ("alpha", "design.md"),
        ("beta", "notes.md"),
    ])
    lookup = getattr(module, "look_up_document_project")
    assert lookup(conn, "alpha") == ["design.md"]
    assert lookup(conn, "' OR 1=1 --") == []


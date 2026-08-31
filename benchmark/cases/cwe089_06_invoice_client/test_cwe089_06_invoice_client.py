from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_06_invoice_client", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_06_invoice_client_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE invoices (client_id TEXT, invoice_ref TEXT)")
    conn.executemany("INSERT INTO invoices (client_id, invoice_ref) VALUES (?, ?)", [
        ("client-a", "inv-100"),
        ("client-b", "inv-200"),
    ])
    lookup = getattr(module, "look_up_invoice_client")
    assert lookup(conn, "client-a") == ["inv-100"]
    assert lookup(conn, "' OR 1=1 --") == []


from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_04_order_customer", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_04_order_customer_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders (customer_id TEXT, order_ref TEXT)")
    conn.executemany("INSERT INTO orders (customer_id, order_ref) VALUES (?, ?)", [
        ("cust-a", "order-100"),
        ("cust-b", "order-200"),
    ])
    lookup = getattr(module, "look_up_order_customer")
    assert lookup(conn, "cust-a") == ["order-100"]
    assert lookup(conn, "' OR 1=1 --") == []


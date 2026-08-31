from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_15_customer_tier", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_15_customer_tier_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE customers (tier TEXT, customer_name TEXT)")
    conn.executemany("INSERT INTO customers (tier, customer_name) VALUES (?, ?)", [
        ("gold", "Orchid Co"),
        ("silver", "Maple Co"),
    ])
    lookup = getattr(module, "look_up_customer_tier")
    assert lookup(conn, "gold") == ["Orchid Co"]
    assert lookup(conn, "' OR 1=1 --") == []


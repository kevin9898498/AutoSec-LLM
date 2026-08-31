from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_13_inventory_sku", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_13_inventory_sku_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE inventory (sku TEXT, item_name TEXT)")
    conn.executemany("INSERT INTO inventory (sku, item_name) VALUES (?, ?)", [
        ("sku-001", "keyboard"),
        ("sku-002", "mouse"),
    ])
    lookup = getattr(module, "look_up_inventory_sku")
    assert lookup(conn, "sku-001") == ["keyboard"]
    assert lookup(conn, "' OR 1=1 --") == []


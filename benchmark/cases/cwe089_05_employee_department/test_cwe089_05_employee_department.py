from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sqlite3


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe089_05_employee_department", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe089_05_employee_department_preserves_lookup_behavior_and_blocks_injection():
    module = _load_target()
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE employees (department TEXT, employee_name TEXT)")
    conn.executemany("INSERT INTO employees (department, employee_name) VALUES (?, ?)", [
        ("engineering", "Lin"),
        ("sales", "Chen"),
    ])
    lookup = getattr(module, "look_up_employee_department")
    assert lookup(conn, "engineering") == ["Lin"]
    assert lookup(conn, "' OR 1=1 --") == []


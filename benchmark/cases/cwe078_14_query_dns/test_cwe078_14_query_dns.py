from __future__ import annotations

import importlib.util
import os
from pathlib import Path


def _load_target():
    target = Path(os.environ.get("SECURE_REPAIR_TARGET", Path(__file__).with_name("secure.py")))
    spec = importlib.util.spec_from_file_location("benchmark_cwe078_14_query_dns", target)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cwe078_14_query_dns_uses_argument_list_without_shell(monkeypatch):
    module = _load_target()
    calls = []

    class Completed:
        stdout = "simulated output"

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return Completed()

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    assert getattr(module, "query_dns")("example.test") == "simulated output"
    assert len(calls) == 1
    assert calls[0][0] == ["dig","example.test"]
    assert calls[0][1]["shell"] is False


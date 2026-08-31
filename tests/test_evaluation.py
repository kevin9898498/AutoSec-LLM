import json

from app.evaluation import load_manifest, run_benchmark, write_report
from app.providers import DemoProvider


def test_batch_evaluation_compares_guided_and_direct_repair(tmp_path):
    source = tmp_path / "vulnerable.py"
    source.write_text(
        """import sqlite3

def login(username, password):
    conn = sqlite3.connect(':memory:')
    query = f\"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'\"
    return conn.execute(query).fetchone()
""",
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"cases": [{
        "id": "sqli-unit",
        "title": "SQL injection unit case",
        "prompt": "Repair this SQLite login function",
        "cwe": "CWE-89",
        "vulnerable_path": "vulnerable.py",
        "expected_rule_ids": ["PY-SQLI-FSTRING"],
    }]}), encoding="utf-8")

    report = run_benchmark(manifest, DemoProvider())
    records = report["cases"]
    assert {row["strategy"] for row in records} == {"sast_guided", "direct_repair"}
    guided = next(row for row in records if row["strategy"] == "sast_guided")
    direct = next(row for row in records if row["strategy"] == "direct_repair")
    assert guided["target_detected"] is True
    assert guided["static_repair_success"] is True
    assert direct["target_detected"] is True
    assert direct["static_repair_success"] is False
    assert report["summary"]["paired_comparison"]["sast_guided_only_successes"] == 1


def test_manifest_inline_code_and_timestamped_reports(tmp_path):
    manifest = tmp_path / "inline.json"
    manifest.write_text(json.dumps({"cases": [{
        "id": "clean-inline",
        "code": "def safe():\n    return 1\n",
        "expected_cwes": ["CWE-89"],
    }]}), encoding="utf-8")
    cases = load_manifest(manifest)
    assert cases[0].inline_code.startswith("def safe")

    report = run_benchmark(manifest, DemoProvider(), strategies=("direct_repair",), max_repairs=0)
    first_json, first_csv = write_report(report, tmp_path / "reports", stem="result")
    second_json, second_csv = write_report(report, tmp_path / "reports", stem="result")
    assert first_json.exists() and first_csv.exists()
    assert second_json.exists() and second_csv.exists()
    assert first_json != second_json

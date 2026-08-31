from app.pipeline import run_pipeline
from app.providers import DemoProvider
from app.scanners import scan_code
from app.validation import check_python_syntax


def test_syntax_gate_reports_invalid_code():
    result = check_python_syntax("def broken(:\n    pass")
    assert not result.valid


def test_builtin_scanner_finds_sqli():
    report = scan_code('cursor.execute(f"SELECT * FROM users WHERE name={name}")')
    assert any(f.cwe == "CWE-89" for f in report.findings)


def test_demo_closed_loop_repairs_login():
    result = run_pipeline("make a SQLite login function", DemoProvider())
    assert result.status == "PASS"
    assert "execute(query, (username, password))" in result.final_code
    assert len(result.attempts) == 2

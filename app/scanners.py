from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .models import Finding, ScanReport, Severity

ROOT = Path(__file__).resolve().parents[1]


def _line(code: str, line_no: int) -> str:
    lines = code.splitlines()
    return lines[line_no - 1] if 0 < line_no <= len(lines) else ""


def _builtin_scan(code: str) -> list[Finding]:
    """Small, deterministic fallback. Semgrep/Bandit remain the primary scanners."""
    findings: list[Finding] = []
    rules = [
        (r"(?:\.execute\(|(?:query|sql|statement)\s*=\s*)f[\"']", "PY-SQLI-FSTRING", "CWE-89", Severity.HIGH,
         "SQL query is composed with an f-string; use parameterized queries."),
        (r"\.execute\([^\n]*%", "PY-SQLI-FORMAT", "CWE-89", Severity.HIGH,
         "SQL query is composed by interpolation; use parameterized queries."),
        (r"subprocess\.(?:run|Popen|call)\([^\n]*shell\s*=\s*True", "PY-CMD-SHELL", "CWE-78", Severity.HIGH,
         "shell=True can enable command injection; pass an argument list with shell=False."),
        (r"^\s*(?:password|secret|api_key)\s*=\s*[\"'][^\"']{4,}[\"']", "PY-HARDCODED-SECRET", "CWE-798", Severity.MEDIUM,
         "Possible hard-coded credential; load it from a secure environment or secret store."),
    ]
    for line_no, source in enumerate(code.splitlines(), 1):
        for pattern, rule_id, cwe, severity, message in rules:
            if re.search(pattern, source, flags=re.IGNORECASE):
                findings.append(Finding(tool="builtin", rule_id=rule_id, cwe=cwe,
                    severity=severity, start_line=line_no, end_line=line_no,
                    message=message, code_excerpt=source.strip()))
    return findings


def _from_semgrep(payload: dict, code: str) -> list[Finding]:
    out: list[Finding] = []
    for item in payload.get("results", []):
        extra = item.get("extra", {})
        meta = extra.get("metadata", {})
        cwe = meta.get("cwe")
        if isinstance(cwe, list):
            cwe = cwe[0] if cwe else None
        level = str(extra.get("severity", "WARNING")).upper()
        severity = Severity.HIGH if level in {"ERROR", "HIGH"} else Severity.MEDIUM
        start = item.get("start", {}).get("line", 1)
        end = item.get("end", {}).get("line", start)
        out.append(Finding(tool="semgrep", rule_id=item.get("check_id", "unknown"), cwe=cwe,
            severity=severity, start_line=start, end_line=end,
            message=extra.get("message", "Semgrep finding"), code_excerpt=_line(code, start)))
    return out


def _from_bandit(payload: dict, code: str) -> list[Finding]:
  out: list[Finding] = []
  for item in payload.get("results", []):
    level = item.get("issue_severity", "MEDIUM").upper()

    # 忽略 LOW 等級的提示（如 import subprocess 的 B404 警告），只抓 MEDIUM 與 HIGH 漏洞
    if level == "LOW":
      continue

    cwe_id = item.get("issue_cwe", {}).get("id")
    cwe = f"CWE-{cwe_id}" if cwe_id else None
    severity = (
        Severity(level)
        if level in Severity._value2member_map_
        else Severity.MEDIUM
    )
    start = int(item.get("line_number", 1))
    out.append(
        Finding(
            tool="bandit",
            rule_id=item.get("test_id", "unknown"),
            cwe=cwe,
            severity=severity,
            start_line=start,
            end_line=start,
            message=item.get("issue_text", "Bandit finding"),
            code_excerpt=_line(code, start),
        )
    )
  return out


def scan_code(code: str) -> ScanReport:
    report = ScanReport()
    # Fallback guarantees an offline demonstration; deduplication happens below.
    report.findings.extend(_builtin_scan(code))
    report.tools_used.append("builtin-demo-rules")
    with tempfile.TemporaryDirectory(prefix="secure-repair-") as temp_dir:
        target = Path(temp_dir) / "generated.py"
        target.write_text(code, encoding="utf-8")
        if shutil.which("semgrep"):
            cmd = ["semgrep", "scan", "--json", "--config", str(ROOT / "rules"), str(target)]
            completed = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            try:
                report.findings.extend(_from_semgrep(json.loads(completed.stdout), code))
                report.tools_used.append("semgrep")
            except json.JSONDecodeError:
                report.errors.append("Semgrep returned non-JSON output.")
        if shutil.which("bandit"):
            cmd = ["bandit", "-q", "-f", "json", str(target)]
            completed = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            try:
                report.findings.extend(_from_bandit(json.loads(completed.stdout), code))
                report.tools_used.append("bandit")
            except json.JSONDecodeError:
                report.errors.append("Bandit returned non-JSON output.")
    unique: dict[tuple[str, int, str], Finding] = {}
    for finding in report.findings:
        key = (finding.cwe or finding.rule_id, finding.start_line, finding.code_excerpt)
        unique.setdefault(key, finding)
    report.findings = list(unique.values())
    return report

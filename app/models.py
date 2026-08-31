from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Finding(BaseModel):
    tool: str
    rule_id: str
    cwe: str | None = None
    severity: Severity = Severity.MEDIUM
    file: str = "generated.py"
    start_line: int = 1
    end_line: int = 1
    message: str
    code_excerpt: str = ""


class SyntaxCheck(BaseModel):
    valid: bool
    error: str | None = None


class ScanReport(BaseModel):
    findings: list[Finding] = Field(default_factory=list)
    tools_used: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class Attempt(BaseModel):
    number: int
    code: str
    syntax: SyntaxCheck
    scan: ScanReport
    note: str


class PipelineResult(BaseModel):
    prompt: str
    original_code: str
    final_code: str
    attempts: list[Attempt]
    status: str
    message: str

    @property
    def original_findings(self) -> list[Finding]:
        return self.attempts[0].scan.findings if self.attempts else []

    @property
    def final_findings(self) -> list[Finding]:
        return self.attempts[-1].scan.findings if self.attempts else []

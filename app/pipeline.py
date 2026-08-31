from __future__ import annotations

from .models import Attempt, PipelineResult
from .providers import LLMProvider
from .scanners import scan_code
from .validation import check_python_syntax


def _acceptable(attempt: Attempt) -> bool:
    # For this research MVP, a run passes only when the syntax gate and all
    # configured SAST rules pass. Production policies may instead allow an
    # explicitly reviewed baseline of accepted findings.
    return attempt.syntax.valid and not attempt.scan.findings


def run_pipeline(prompt: str, provider: LLMProvider, initial_code: str | None = None, max_repairs: int = 2) -> PipelineResult:
    code = initial_code.strip() if initial_code and initial_code.strip() else provider.generate(prompt)
    attempts: list[Attempt] = []
    for number in range(max_repairs + 1):
        syntax = check_python_syntax(code)
        scan = scan_code(code) if syntax.valid else scan_code("")
        note = "Generated code" if number == 0 else "Repaired code"
        if not syntax.valid:
            note = f"Syntax gate failed: {syntax.error}"
        attempt = Attempt(number=number, code=code, syntax=syntax, scan=scan, note=note)
        attempts.append(attempt)
        if _acceptable(attempt):
            return PipelineResult(prompt=prompt, original_code=attempts[0].code, final_code=code,
                attempts=attempts, status="PASS", message="Syntax and security gates passed.")
        if number == max_repairs:
            break
        feedback = syntax.error or "Target findings remain or new high-severity findings were introduced."
        code = provider.repair(code, scan.findings, feedback)
    return PipelineResult(prompt=prompt, original_code=attempts[0].code, final_code=code,
        attempts=attempts, status="NEEDS_REVIEW", message="Retry limit reached; a human review is required.")

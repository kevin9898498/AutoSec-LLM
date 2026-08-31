from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_pipeline
from .providers import get_provider


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM secure-repair closed-loop MVP")
    parser.add_argument("--prompt", default="Write a SQLite login function")
    parser.add_argument("--code", help="Path to Python source to scan and repair")
    parser.add_argument("--openai", action="store_true", help="Use OpenAI instead of offline demo provider")
    parser.add_argument("--max-repairs", type=int, default=2)
    args = parser.parse_args()
    source = Path(args.code).read_text(encoding="utf-8") if args.code else None
    result = run_pipeline(args.prompt, get_provider(args.openai), source, args.max_repairs)
    print(f"{result.status}: {result.message}")
    for attempt in result.attempts:
        print(f"attempt={attempt.number} syntax={attempt.syntax.valid} findings={len(attempt.scan.findings)}")
        for finding in attempt.scan.findings:
            print(f"  {finding.severity} {finding.cwe or finding.rule_id} L{finding.start_line}: {finding.message}")


if __name__ == "__main__":
    main()

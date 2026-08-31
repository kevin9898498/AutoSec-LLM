"""Command-line entry point for paired SAST-guided repair evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .evaluation import run_benchmark, write_report
from .providers import get_provider


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare SAST-guided LLM repair against direct no-SAST repair on a benchmark."
    )
    parser.add_argument("--manifest", required=True, help="Path to JSON, JSONL, or optional YAML benchmark manifest")
    parser.add_argument("--output-dir", default="evaluation-results", help="Directory for timestamped JSON and CSV reports")
    parser.add_argument("--max-repairs", type=int, default=2, help="Maximum repair calls after the initial candidate")
    parser.add_argument("--openai", action="store_true", help="Use OpenAI provider instead of the deterministic offline demo")
    parser.add_argument(
        "--strategy",
        choices=("both", "sast_guided", "direct_repair"),
        default="both",
        help="Repair condition(s) to evaluate",
    )
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Run controlled pytest files against temporary repaired code via SECURE_REPAIR_TARGET",
    )
    parser.add_argument("--test-timeout", type=int, default=30, help="Per-case pytest timeout in seconds")
    args = parser.parse_args()
    if args.max_repairs < 0:
        parser.error("--max-repairs must be non-negative")
    if args.test_timeout <= 0:
        parser.error("--test-timeout must be positive")

    strategies = ("sast_guided", "direct_repair") if args.strategy == "both" else (args.strategy,)
    provider = get_provider(args.openai)
    report = run_benchmark(
        args.manifest,
        provider,
        strategies=strategies,
        max_repairs=args.max_repairs,
        run_tests=args.run_tests,
        test_timeout_seconds=args.test_timeout,
    )
    json_path, csv_path = write_report(report, Path(args.output_dir))
    print(f"JSON report: {json_path}")
    print(f"CSV report:  {csv_path}")
    for strategy, summary in report["summary"]["by_strategy"].items():
        print(
            f"{strategy}: static_success={summary['static_repair_success_rate']} "
            f"syntax={summary['final_syntax_valid_rate']} "
            f"new_findings={summary['security_regression_rate']}"
        )
    paired = report["summary"].get("paired_comparison", {})
    if paired:
        print("paired comparison:", paired)


if __name__ == "__main__":
    main()

"""CLI entrypoint for the end-to-end margin-call demo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from margin_call_demo import DemoExecutionError, run_margin_call_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the end-to-end margin-call demo and emit execution-report artifacts."
        )
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the margin-call demo manifest JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where generated execution artifacts should be written.",
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[2],
        help="Repository root used for relative artifact references.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        report = run_margin_call_demo(
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
        )
    except (DemoExecutionError, OSError, ValueError) as exc:
        print(f"demo-margin-call: {exc}", file=sys.stderr)
        return 1

    print(report["artifacts"]["executionReportPath"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

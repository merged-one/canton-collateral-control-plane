"""CLI entrypoint for the end-to-end substitution demo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from substitution_demo import DemoExecutionError, run_substitution_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the end-to-end substitution demo and emit substitution-report artifacts."
        )
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the substitution demo manifest JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where generated substitution artifacts should be written.",
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[2],
        help="Repository root used for relative artifact references.",
    )
    parser.add_argument(
        "--runtime",
        default="IDE_LEDGER",
        choices=["IDE_LEDGER", "QUICKSTART"],
        help="Substitution workflow runtime to use.",
    )
    parser.add_argument(
        "--report-basename",
        default=None,
        help="Optional basename for generated substitution-report, summary, and timeline files.",
    )
    parser.add_argument(
        "--command-name",
        default=None,
        help="Optional command string recorded inside the generated substitution report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        report = run_substitution_demo(
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
            runtime_mode=args.runtime,
            report_basename=args.report_basename,
            command_name=args.command_name,
        )
    except (DemoExecutionError, OSError, ValueError) as exc:
        print(f"demo-substitution: {exc}", file=sys.stderr)
        return 1

    print(report["artifacts"]["substitutionReportPath"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

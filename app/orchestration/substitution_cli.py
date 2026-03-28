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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        report = run_substitution_demo(
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
        )
    except (DemoExecutionError, OSError, ValueError) as exc:
        print(f"demo-substitution: {exc}", file=sys.stderr)
        return 1

    print(report["artifacts"]["substitutionReportPath"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

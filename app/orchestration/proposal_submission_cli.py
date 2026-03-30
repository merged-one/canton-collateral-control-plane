"""CLI entrypoint for the proposal submission package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from margin_call_demo import DemoExecutionError
from proposal_submission_pack import build_proposal_submission_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build the reviewer-facing proposal submission package from the final demo pack."
        )
    )
    parser.add_argument(
        "--final-demo-pack",
        required=True,
        help="Path to the generated final demo-pack JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where generated proposal-submission artifacts should be written.",
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
        report = build_proposal_submission_package(
            final_demo_pack_path=args.final_demo_pack,
            output_dir=args.output_dir,
            repo_root=args.repo_root,
        )
    except (DemoExecutionError, OSError, ValueError) as exc:
        print(f"proposal-package: {exc}", file=sys.stderr)
        return 1

    print(report["artifacts"]["proposalSubmissionManifestPath"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

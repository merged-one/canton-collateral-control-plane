"""CLI entrypoint for CPL v0.1 policy evaluation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from evaluator import (
    InventoryInputError,
    default_output_path,
    evaluate_policy,
    load_json,
    write_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate a CPL v0.1 policy against a candidate collateral inventory set."
    )
    parser.add_argument("--policy", required=True, help="Path to the CPL policy JSON file.")
    parser.add_argument(
        "--inventory",
        required=True,
        help="Path to the candidate inventory JSON file.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path for the generated policy evaluation report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        policy = load_json(args.policy)
        inventory = load_json(args.inventory)
        report = evaluate_policy(policy, inventory)
    except (OSError, ValueError, InventoryInputError) as exc:
        print(f"policy-eval: {exc}", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else default_output_path(report)
    written_path = write_report(report, output_path)
    print(written_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run schemathesis with common flags for OpenAPI testing."""

from __future__ import annotations

import argparse
import subprocess


def build_command(args: argparse.Namespace) -> list[str]:
    command = ["schemathesis", "run", args.schema]
    if args.base_url:
        command.extend(["--url", args.base_url])
    if args.auth_header:
        command.extend(["--header", f"Authorization: Bearer {args.auth_header}"])
    if args.max_examples:
        command.extend(["--max-examples", str(args.max_examples)])
    if args.continue_on_failure:
        command.append("--continue-on-failure")
    return command


def main() -> None:
    parser = argparse.ArgumentParser(description="Run schemathesis against an OpenAPI schema")
    parser.add_argument("schema", help="Path or URL to OpenAPI schema")
    parser.add_argument("--base-url", help="Base URL for file-based schemas")
    parser.add_argument("--auth-header", help="Bearer token value")
    parser.add_argument("--max-examples", type=int, default=50)
    parser.add_argument("--continue-on-failure", action="store_true")

    args = parser.parse_args()
    command = build_command(args)
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    main()

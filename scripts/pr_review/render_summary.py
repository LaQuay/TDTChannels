#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from reporting import render_summary


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Render the catalog validation GitHub job summary")
    parser.add_argument("--report-file", required=True)
    parser.add_argument("--unit-tests", required=True)
    parser.add_argument("--deterministic-validation", required=True)
    parser.add_argument("--network-checks", required=True)
    args = parser.parse_args()
    print(
        render_summary(
            args.report_file,
            unit_tests=args.unit_tests,
            deterministic_validation=args.deterministic_validation,
            network_checks=args.network_checks,
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

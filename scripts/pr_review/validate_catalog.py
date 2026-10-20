#!/usr/bin/env python3
"""Validate catalog entries changed by a pull request."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
from typing import Sequence

from catalog import CATALOGS, changed_entries, links_in, new_validation_problems, parse_catalog
from duplicates import new_duplicate_problems
from git_changes import added_line_numbers, base_catalog, catalog_diff
from models import DUPLICATE_CHECKS, ENTRY_CHECKS, ROW_STRUCTURE, Entry, Problem
from network_checks import network_warnings
from reporting import build_report, write_report


def run(base_revision: str, run_network: bool, report_file: str | None = None) -> int:
    head_entries: list[Entry] = []
    base_entries: list[Entry] = []
    changed: list[Entry] = []
    problems: list[Problem] = []
    attempted: set[str] = set()
    catalog_changed = False

    for catalog in CATALOGS:
        path = Path(catalog)
        if not path.is_file():
            catalog_changed = True
            attempted.add(ROW_STRUCTURE)
            problems.append(Problem(catalog, 1, ROW_STRUCTURE, "catalog file is missing"))
            continue
        head_text = path.read_text(encoding="utf-8")
        base_text = base_catalog(base_revision, catalog)
        head_catalog_entries, _ = parse_catalog(catalog, head_text)
        base_catalog_entries, _ = parse_catalog(catalog, base_text)
        head_entries.extend(head_catalog_entries)
        base_entries.extend(base_catalog_entries)
        line_numbers = added_line_numbers(catalog_diff(base_revision, catalog))
        if line_numbers:
            catalog_changed = True
            attempted.add(ROW_STRUCTURE)
        selected, selected_problems = changed_entries(catalog, head_text, line_numbers)
        if selected:
            attempted.update(ENTRY_CHECKS)
        changed.extend(selected)
        problems.extend(new_validation_problems(base_catalog_entries, selected, selected_problems))

    if catalog_changed:
        attempted.update(DUPLICATE_CHECKS)
    problems.extend(new_duplicate_problems(base_entries, head_entries))
    unique_problems = sorted(set(problems), key=lambda item: (item.catalog, item.line, item.check, item.message))
    for problem in unique_problems:
        print(problem.render())
    if unique_problems:
        if report_file:
            write_report(
                report_file,
                build_report(
                    attempted=attempted,
                    problems=unique_problems,
                    changed_entries=len(changed),
                    network_ran=False,
                    network_attempted=False,
                    network_warnings=0,
                ),
            )
        print(f"Catalog validation failed with {len(unique_problems)} error(s).")
        return 1

    noun = "entry" if len(changed) == 1 else "entries"
    print(f"Catalog validation passed for {len(changed)} added or modified {noun}.")
    warnings: list[Problem] = []
    network_attempted = False
    if run_network:
        network_attempted = any(links_in(entry.stream) for entry in changed)
        warnings = network_warnings(changed)
        for warning in warnings:
            print(warning.render("warning"))
        print(f"Advisory network checks completed with {len(warnings)} warning(s).")
    if report_file:
        write_report(
            report_file,
            build_report(
                attempted=attempted,
                problems=unique_problems,
                changed_entries=len(changed),
                network_ran=run_network,
                network_attempted=network_attempted,
                network_warnings=len(warnings),
            ),
        )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-revision",
        default=os.environ.get("GITHUB_BASE_SHA"),
        help="Git revision to compare against (or set GITHUB_BASE_SHA)",
    )
    parser.add_argument("--network", action="store_true", help="run advisory checks for changed stream URLs")
    parser.add_argument("--report-file", help="write structured validation results as JSON")
    args = parser.parse_args(argv)
    if not args.base_revision:
        parser.error("--base-revision is required when GITHUB_BASE_SHA is not set")
    try:
        return run(args.base_revision, args.network, args.report_file)
    except (OSError, RuntimeError, UnicodeError) as error:
        print(f"Catalog validator could not run: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

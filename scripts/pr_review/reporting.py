from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from models import CHECKS, STREAM_AVAILABILITY, Problem


def build_report(
    *,
    attempted: set[str],
    problems: Sequence[Problem],
    changed_entries: int,
    network_ran: bool,
    network_attempted: bool,
    network_warnings: int,
) -> dict[str, object]:
    failed = {problem.check for problem in problems}
    checks = {
        check: {
            "label": label,
            "blocking": blocking,
            "status": "failed" if check in failed else "passed" if check in attempted else "not_applicable",
        }
        for check, label, blocking in CHECKS
    }
    if not network_ran:
        network_status = "not_run"
    elif not network_attempted:
        network_status = "not_applicable"
    elif network_warnings:
        network_status = "warnings"
    else:
        network_status = "passed"
    checks[STREAM_AVAILABILITY] = {
        "label": "Stream availability",
        "blocking": False,
        "status": network_status,
        "warnings": network_warnings,
    }
    return {"changed_entries": changed_entries, "checks": checks}


def write_report(path: str, report: dict[str, object]) -> None:
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")


def _workflow_result(outcome: str) -> str:
    return {
        "success": "✅ Passed",
        "failure": "❌ Failed",
        "cancelled": "⏹️ Cancelled",
        "skipped": "⏭️ Not run",
    }.get(outcome, "⏭️ Not run")


def _check_result(check: dict[str, object]) -> str:
    status = check.get("status")
    if status == "passed":
        return "✅ Passed"
    if status == "failed":
        return "❌ Failed"
    if status == "warnings":
        count = int(check.get("warnings", 0))
        noun = "warning" if count == 1 else "warnings"
        return f"⚠️ {count} {noun}"
    if status == "step_failed":
        return "⚠️ Check failed"
    if status == "not_applicable":
        return "➖ Not applicable"
    return "⏭️ Not run"


def render_summary(
    report_path: str,
    *,
    unit_tests: str,
    deterministic_validation: str,
    network_checks: str,
) -> str:
    path = Path(report_path)
    report = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {"checks": {}}
    checks = report.get("checks", {})
    lines = [
        "## Catalog validation",
        "",
        "| Check | Result | Blocking |",
        "| --- | --- | --- |",
    ]
    for check, label, blocking in CHECKS:
        details = checks.get(check, {"status": "not_run"})
        lines.append(f"| {label} | {_check_result(details)} | {'Yes' if blocking else 'No'} |")
    network = checks.get(STREAM_AVAILABILITY, {"status": "not_run"})
    if network_checks == "failure" and network.get("status") == "not_run":
        network = {"status": "step_failed"}
    lines.extend(
        [
            f"| Stream availability | {_check_result(network)} | No |",
            "",
            f"Changed catalog entries: **{report.get('changed_entries', 0)}**",
            "",
            "### Workflow health",
            "",
            f"- Validator self-tests: {_workflow_result(unit_tests)}",
            f"- Deterministic validation step: {_workflow_result(deterministic_validation)}",
            f"- Advisory network step: {_workflow_result(network_checks)}",
            "",
            "Stream availability is advisory because streams may be geo-restricted or reject GitHub-hosted runners.",
        ]
    )
    return "\n".join(lines) + "\n"

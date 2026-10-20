from __future__ import annotations

import re
import subprocess
from typing import Sequence


HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def added_line_numbers(diff: str) -> set[int]:
    result: set[int] = set()
    head_line: int | None = None
    for line in diff.splitlines():
        hunk = HUNK_RE.match(line)
        if hunk:
            head_line = int(hunk.group(1))
            continue
        if head_line is None or line.startswith("\\ No newline"):
            continue
        if line.startswith("+") and not line.startswith("+++"):
            result.add(head_line)
            head_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            continue
        else:
            head_line += 1
    return result


def git_output(arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        detail = completed.stderr.strip() or "unknown Git error"
        raise RuntimeError(f"git {' '.join(arguments)} failed: {detail}")
    return completed.stdout


def base_catalog(base_revision: str, catalog: str) -> str:
    return git_output(["show", f"{base_revision}:{catalog}"])


def catalog_diff(base_revision: str, catalog: str) -> str:
    return git_output(["diff", "--unified=0", "--no-ext-diff", base_revision, "--", catalog])

from __future__ import annotations

import collections
from typing import Sequence

from catalog import links_in, normalized
from models import DUPLICATE_EPG_IDS, DUPLICATE_NAMES, DUPLICATE_STREAM_URLS, Entry, Problem


def _duplicate_values(entries: Sequence[Entry], kind: str) -> dict[tuple[str, str], list[Entry]]:
    values: dict[tuple[str, str], list[Entry]] = collections.defaultdict(list)
    for entry in entries:
        if kind == "name":
            key_values = [normalized(entry.name)]
            scope = entry.catalog
        elif kind == "stream URL":
            key_values = [url for _, url in links_in(entry.stream)]
            scope = "all catalogs"
        elif kind == "EPG ID":
            key_values = [] if entry.epg_id == "-" else [normalized(entry.epg_id)]
            scope = "all catalogs"
        else:  # pragma: no cover - internal programming error
            raise ValueError(kind)
        for value in set(key_values):
            if value:
                values[(scope, value)].append(entry)
    return values


def new_duplicate_problems(
    base_entries: Sequence[Entry], head_entries: Sequence[Entry]
) -> list[Problem]:
    problems: list[Problem] = []
    kinds = (
        ("name", DUPLICATE_NAMES),
        ("stream URL", DUPLICATE_STREAM_URLS),
        ("EPG ID", DUPLICATE_EPG_IDS),
    )
    for kind, check in kinds:
        base = _duplicate_values(base_entries, kind)
        head = _duplicate_values(head_entries, kind)
        for key, duplicate_entries in head.items():
            if len(duplicate_entries) <= 1 or len(duplicate_entries) <= len(base.get(key, [])):
                continue
            locations = ", ".join(f"{item.catalog}:{item.line}" for item in duplicate_entries)
            for entry in duplicate_entries:
                problems.append(
                    Problem(entry.catalog, entry.line, check, f"new duplicate {kind} (also at {locations})")
                )
    return problems

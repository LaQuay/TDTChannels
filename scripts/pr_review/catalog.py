from __future__ import annotations

import re
from typing import Sequence
import urllib.parse

from models import EPG_ID, INFO_TAGS, LOGO_FORMAT, NAME, ROW_STRUCTURE, STREAM_FORMAT, WEB_FORMAT, Entry, Problem


CATALOGS = ("TELEVISION.md", "RADIO.md")
EXPECTED_HEADERS = {
    "TELEVISION.md": "| Canal | M3U8 | Web | Logo | EPG ID | Info |",
    "RADIO.md": "| Emisoras | Stream | Web | Logo | EPG ID | Info |",
}
SEPARATOR_RE = re.compile(r"^\|(?:\s*:?-+:?\s*\|){6}$")
LINK_START_RE = re.compile(r"\[([^\]]+)\]\((https?://)", re.IGNORECASE)
INFO_RE = re.compile(r"[A-Z0-9]+(?:,[A-Z0-9]+)*")
SPACE_RE = re.compile(r"\s+")
STREAM_LABELS = {
    "TELEVISION.md": {"m3u8", "mpd", "stream", "youtube"},
    "RADIO.md": {"aac", "m3u8", "m3u", "mp3", "mpd", "ogg", "stream", "youtube"},
}


def normalized(value: str) -> str:
    return SPACE_RE.sub(" ", value.strip()).casefold()


def split_row(line: str) -> list[str] | None:
    if not line.startswith("|") or not line.endswith("|"):
        return None
    return [cell.strip() for cell in line[1:-1].split("|")]


def links_in(cell: str) -> list[tuple[str, str]]:
    return [(label, url) for label, url, _, _ in _parsed_links(cell)]


def _parsed_links(cell: str) -> list[tuple[str, str, int, int]]:
    """Return Markdown links while allowing balanced parentheses inside URLs."""
    links: list[tuple[str, str, int, int]] = []
    cursor = 0
    while match := LINK_START_RE.search(cell, cursor):
        url_start = match.end() - len(match.group(2))
        depth = 1
        position = match.end()
        while position < len(cell):
            character = cell[position]
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    url = cell[url_start:position]
                    if not any(character.isspace() for character in url):
                        links.append((match.group(1).strip(), url, match.start(), position + 1))
                    cursor = position + 1
                    break
            position += 1
        else:
            break
    return links


def _validate_link_cell(
    entry: Entry,
    cell: str,
    field: str,
    check: str,
    allowed_labels: set[str],
    *,
    allow_dash: bool,
    exactly_one: bool = False,
) -> list[Problem]:
    if cell == "-":
        return [] if allow_dash else [Problem(entry.catalog, entry.line, check, f"{field} may not be '-'")]
    matches = _parsed_links(cell)
    if not matches:
        return [Problem(entry.catalog, entry.line, check, f"{field} must contain an HTTP(S) Markdown link")]
    if exactly_one and len(matches) != 1:
        return [Problem(entry.catalog, entry.line, check, f"{field} must contain exactly one Markdown link")]

    problems: list[Problem] = []
    cursor = 0
    for index, (link_text, url, start, end) in enumerate(matches):
        separator = cell[cursor:start].strip()
        if separator != ("" if index == 0 else "-"):
            problems.append(Problem(entry.catalog, entry.line, check, f"{field} links must be separated by ' - '"))
            break
        label = link_text.split(maxsplit=1)[0].casefold()
        if label not in allowed_labels:
            allowed = ", ".join(sorted(allowed_labels))
            problems.append(
                Problem(entry.catalog, entry.line, check, f"unsupported {field} link label '{label}' (expected: {allowed})")
            )
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            problems.append(Problem(entry.catalog, entry.line, check, f"{field} link must be an absolute HTTP(S) URL"))
        elif parsed.username is not None or parsed.password is not None:
            problems.append(Problem(entry.catalog, entry.line, check, f"{field} link must not contain embedded credentials"))
        cursor = end
    if cell[cursor:].strip():
        problems.append(Problem(entry.catalog, entry.line, check, f"unexpected text after the final {field} link"))
    return problems


def validate_entry(entry: Entry) -> list[Problem]:
    problems: list[Problem] = []
    if not entry.name or entry.name == "-":
        problems.append(Problem(entry.catalog, entry.line, NAME, "channel or station name is required"))
    problems.extend(
        _validate_link_cell(entry, entry.stream, "stream", STREAM_FORMAT, STREAM_LABELS[entry.catalog], allow_dash=True)
    )
    problems.extend(
        _validate_link_cell(entry, entry.web, "web", WEB_FORMAT, {"web"}, allow_dash=False, exactly_one=True)
    )
    problems.extend(
        _validate_link_cell(entry, entry.logo, "logo", LOGO_FORMAT, {"logo"}, allow_dash=False, exactly_one=True)
    )
    if not entry.epg_id:
        problems.append(Problem(entry.catalog, entry.line, EPG_ID, "EPG ID must be '-' or a value"))
    if not entry.info or (entry.info != "-" and not INFO_RE.fullmatch(entry.info)):
        problems.append(
            Problem(entry.catalog, entry.line, INFO_TAGS, "Info must be '-' or comma-separated uppercase tags without spaces")
        )
    return problems


def parse_catalog(catalog: str, text: str) -> tuple[list[Entry], list[Problem]]:
    entries: list[Entry] = []
    problems: list[Problem] = []
    section = ""
    expected_header = EXPECTED_HEADERS[catalog]
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.startswith("##"):
            section = line.lstrip("#").strip()
        if not line.startswith("|") or line == expected_header or SEPARATOR_RE.fullmatch(line):
            continue
        cells = split_row(line)
        if cells is None or len(cells) != 6:
            problems.append(
                Problem(catalog, line_number, ROW_STRUCTURE, "catalog rows must have exactly six pipe-delimited columns")
            )
            continue
        entries.append(Entry(catalog, line_number, section, *cells))
    return entries, problems


def changed_entries(
    catalog: str, text: str, changed_lines: set[int]
) -> tuple[list[Entry], list[Problem]]:
    entries, parse_problems = parse_catalog(catalog, text)
    selected = [entry for entry in entries if entry.line in changed_lines]
    problems = [problem for problem in parse_problems if problem.line in changed_lines]
    entry_lines = {entry.line for entry in selected}
    expected_header = EXPECTED_HEADERS[catalog]
    lines = text.splitlines()
    for line_number in sorted(changed_lines):
        if line_number < 1 or line_number > len(lines):
            continue
        line = lines[line_number - 1]
        if line.startswith("|"):
            if (
                line_number not in entry_lines
                and line != expected_header
                and not SEPARATOR_RE.fullmatch(line)
                and not any(problem.line == line_number for problem in problems)
            ):
                problems.append(Problem(catalog, line_number, ROW_STRUCTURE, "unrecognized or malformed catalog table row"))
        elif line.strip() and _line_is_in_table_block(lines, line_number, expected_header):
            problems.append(Problem(catalog, line_number, ROW_STRUCTURE, "catalog table rows must start and end with a pipe"))
        elif not line.strip() and _blank_splits_table(lines, line_number):
            problems.append(Problem(catalog, line_number, ROW_STRUCTURE, "blank line splits a catalog table"))
    for entry in selected:
        problems.extend(validate_entry(entry))
    return selected, problems


def _line_is_in_table_block(lines: Sequence[str], line_number: int, expected_header: str) -> bool:
    index = line_number - 1
    start = index
    while start > 0 and lines[start - 1].strip():
        start -= 1
    end = index + 1
    while end < len(lines) and lines[end].strip():
        end += 1
    return expected_header in lines[start:end]


def _blank_splits_table(lines: Sequence[str], line_number: int) -> bool:
    index = line_number - 1
    if index == 0 or index + 1 >= len(lines):
        return False
    return split_row(lines[index - 1]) is not None and split_row(lines[index + 1]) is not None


def _problem_fingerprint(entry: Entry, problem: Problem) -> tuple[str, str, str]:
    message = problem.message
    if "stream" in message:
        value = entry.stream
    elif "web" in message:
        value = entry.web
    elif "logo" in message:
        value = entry.logo
    elif message.startswith("EPG ID"):
        value = entry.epg_id
    elif message.startswith("Info"):
        value = entry.info
    else:
        value = entry.name
    return entry.catalog, value, message


def new_validation_problems(
    base_entries: Sequence[Entry], changed: Sequence[Entry], problems: Sequence[Problem]
) -> list[Problem]:
    """Grandfather a legacy error only while its offending field is unchanged."""
    baseline = {
        _problem_fingerprint(entry, problem)
        for entry in base_entries
        for problem in validate_entry(entry)
    }
    changed_by_location = {(entry.catalog, entry.line): entry for entry in changed}
    result: list[Problem] = []
    for problem in problems:
        entry = changed_by_location.get((problem.catalog, problem.line))
        if entry is None or _problem_fingerprint(entry, problem) not in baseline:
            result.append(problem)
    return result

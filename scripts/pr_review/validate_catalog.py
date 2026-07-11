#!/usr/bin/env python3
"""Validate catalog entries changed by a pull request.

Deterministic validation failures are blocking. Optional network checks only emit
warnings and always remain advisory.
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import dataclasses
import ipaddress
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
from typing import Sequence
import urllib.error
import urllib.parse
import urllib.request


CATALOGS = ("TELEVISION.md", "RADIO.md")
EXPECTED_HEADERS = {
    "TELEVISION.md": "| Canal | M3U8 | Web | Logo | EPG ID | Info |",
    "RADIO.md": "| Emisoras | Stream | Web | Logo | EPG ID | Info |",
}
SEPARATOR_RE = re.compile(r"^\|(?:\s*:?-+:?\s*\|){6}$")
LINK_START_RE = re.compile(r"\[([^\]]+)\]\((https?://)", re.IGNORECASE)
INFO_RE = re.compile(r"[A-Z0-9]+(?:,[A-Z0-9]+)*")
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
SPACE_RE = re.compile(r"\s+")

STREAM_LABELS = {
    "TELEVISION.md": {"m3u8", "mpd", "stream", "youtube"},
    "RADIO.md": {"aac", "m3u8", "m3u", "mp3", "mpd", "ogg", "stream", "youtube"},
}
USER_AGENT = "TDTChannels-PR-Validator/1.0 (+https://github.com/LaQuay/TDTChannels)"
NETWORK_TIMEOUT_SECONDS = 5
NETWORK_RESPONSE_LIMIT = 64 * 1024
NETWORK_URL_LIMIT = 20


@dataclasses.dataclass(frozen=True)
class Entry:
    catalog: str
    line: int
    section: str
    name: str
    stream: str
    web: str
    logo: str
    epg_id: str
    info: str


@dataclasses.dataclass(frozen=True)
class Problem:
    catalog: str
    line: int
    message: str

    def render(self, level: str = "error") -> str:
        return f"::{level} file={self.catalog},line={self.line}::{self.message}"


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
    allowed_labels: set[str],
    *,
    allow_dash: bool,
    exactly_one: bool = False,
) -> list[Problem]:
    if cell == "-":
        return [] if allow_dash else [Problem(entry.catalog, entry.line, f"{field} may not be '-'")]

    matches = _parsed_links(cell)
    if not matches:
        return [Problem(entry.catalog, entry.line, f"{field} must contain an HTTP(S) Markdown link")]
    if exactly_one and len(matches) != 1:
        return [Problem(entry.catalog, entry.line, f"{field} must contain exactly one Markdown link")]

    problems: list[Problem] = []
    cursor = 0
    for index, (link_text, url, start, end) in enumerate(matches):
        separator = cell[cursor:start].strip()
        if separator != ("" if index == 0 else "-"):
            problems.append(
                Problem(entry.catalog, entry.line, f"{field} links must be separated by ' - '")
            )
            break
        label = link_text.split(maxsplit=1)[0].casefold()
        if label not in allowed_labels:
            allowed = ", ".join(sorted(allowed_labels))
            problems.append(
                Problem(entry.catalog, entry.line, f"unsupported {field} link label '{label}' (expected: {allowed})")
            )
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            problems.append(Problem(entry.catalog, entry.line, f"{field} link must be an absolute HTTP(S) URL"))
        elif parsed.username is not None or parsed.password is not None:
            problems.append(Problem(entry.catalog, entry.line, f"{field} link must not contain embedded credentials"))
        cursor = end
    if cell[cursor:].strip():
        problems.append(Problem(entry.catalog, entry.line, f"unexpected text after the final {field} link"))
    return problems


def validate_entry(entry: Entry) -> list[Problem]:
    problems: list[Problem] = []
    if not entry.name or entry.name == "-":
        problems.append(Problem(entry.catalog, entry.line, "channel or station name is required"))
    problems.extend(
        _validate_link_cell(
            entry,
            entry.stream,
            "stream",
            STREAM_LABELS[entry.catalog],
            allow_dash=True,
        )
    )
    problems.extend(
        _validate_link_cell(entry, entry.web, "web", {"web"}, allow_dash=False, exactly_one=True)
    )
    problems.extend(
        _validate_link_cell(entry, entry.logo, "logo", {"logo"}, allow_dash=False, exactly_one=True)
    )
    if not entry.epg_id:
        problems.append(Problem(entry.catalog, entry.line, "EPG ID must be '-' or a value"))
    if not entry.info or (entry.info != "-" and not INFO_RE.fullmatch(entry.info)):
        problems.append(
            Problem(entry.catalog, entry.line, "Info must be '-' or comma-separated uppercase tags without spaces")
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
                Problem(catalog, line_number, "catalog rows must have exactly six pipe-delimited columns")
            )
            continue
        entries.append(Entry(catalog, line_number, section, *cells))
    return entries, problems


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
            ):
                if not any(problem.line == line_number for problem in problems):
                    problems.append(
                        Problem(catalog, line_number, "unrecognized or malformed catalog table row")
                    )
        elif line.strip() and _line_is_in_table_block(lines, line_number, expected_header):
            problems.append(
                Problem(catalog, line_number, "catalog table rows must start and end with a pipe")
            )
        elif not line.strip() and _blank_splits_table(lines, line_number):
            problems.append(Problem(catalog, line_number, "blank line splits a catalog table"))
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
    previous = split_row(lines[index - 1])
    following = split_row(lines[index + 1])
    return previous is not None and following is not None


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
    for kind in ("name", "stream URL", "EPG ID"):
        base = _duplicate_values(base_entries, kind)
        head = _duplicate_values(head_entries, kind)
        for key, duplicate_entries in head.items():
            if len(duplicate_entries) <= 1 or len(duplicate_entries) <= len(base.get(key, [])):
                continue
            locations = ", ".join(f"{item.catalog}:{item.line}" for item in duplicate_entries)
            for entry in duplicate_entries:
                problems.append(
                    Problem(entry.catalog, entry.line, f"new duplicate {kind} (also at {locations})")
                )
    return problems


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


def _public_addresses(hostname: str) -> tuple[bool, str | None]:
    if hostname.casefold() == "localhost" or hostname.casefold().endswith(".localhost"):
        return False, "local destinations are not probed"
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(hostname, None)}
    except OSError as error:
        return False, f"DNS lookup failed ({error.__class__.__name__})"
    for address in addresses:
        parsed = ipaddress.ip_address(address)
        if not parsed.is_global:
            return False, "private or non-global destinations are not probed"
    return True, None


def check_url(url: str) -> str | None:
    parsed = urllib.parse.urlsplit(url)
    if not parsed.hostname:
        return "URL has no hostname"
    safe, reason = _public_addresses(parsed.hostname)
    if not safe:
        return reason
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Range": f"bytes=0-{NETWORK_RESPONSE_LIMIT - 1}",
        },
    )
    try:
        with _safe_urlopen(request, timeout=NETWORK_TIMEOUT_SECONDS) as response:
            response.read(NETWORK_RESPONSE_LIMIT + 1)
            status = getattr(response, "status", 200)
            if status >= 400:
                return f"HTTP {status}"
    except urllib.error.HTTPError as error:
        return f"HTTP {error.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return f"request failed ({error.__class__.__name__})"
    return None


class _PublicRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        hostname = urllib.parse.urlsplit(new_url).hostname
        if not hostname:
            raise urllib.error.URLError("redirect has no hostname")
        safe, reason = _public_addresses(hostname)
        if not safe:
            raise urllib.error.URLError(reason or "unsafe redirect destination")
        return super().redirect_request(request, fp, code, message, headers, new_url)


def _safe_urlopen(request: urllib.request.Request, *, timeout: int):
    opener = urllib.request.build_opener(_PublicRedirectHandler())
    return opener.open(request, timeout=timeout)


def network_warnings(entries: Sequence[Entry]) -> list[Problem]:
    targets: list[tuple[Entry, str]] = []
    seen: set[str] = set()
    for entry in entries:
        for _, url in links_in(entry.stream):
            if url not in seen:
                seen.add(url)
                targets.append((entry, url))
    omitted = max(0, len(targets) - NETWORK_URL_LIMIT)
    targets = targets[:NETWORK_URL_LIMIT]
    warnings: list[Problem] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(check_url, url): entry for entry, url in targets}
        for future in concurrent.futures.as_completed(futures):
            entry = futures[future]
            try:
                message = future.result()
            except Exception as error:  # advisory checks must never break validation
                message = f"unexpected check failure ({error.__class__.__name__})"
            if message:
                warnings.append(Problem(entry.catalog, entry.line, f"advisory stream check: {message}"))
    if omitted and entries:
        warnings.append(
            Problem(entries[0].catalog, entries[0].line, f"advisory stream check skipped {omitted} URLs after the safety limit")
        )
    return sorted(warnings, key=lambda item: (item.catalog, item.line, item.message))


def run(base_revision: str, run_network: bool) -> int:
    head_entries: list[Entry] = []
    base_entries: list[Entry] = []
    changed: list[Entry] = []
    problems: list[Problem] = []

    for catalog in CATALOGS:
        path = Path(catalog)
        if not path.is_file():
            problems.append(Problem(catalog, 1, "catalog file is missing"))
            continue
        head_text = path.read_text(encoding="utf-8")
        base_text = base_catalog(base_revision, catalog)
        head_catalog_entries, _ = parse_catalog(catalog, head_text)
        base_catalog_entries, _ = parse_catalog(catalog, base_text)
        head_entries.extend(head_catalog_entries)
        base_entries.extend(base_catalog_entries)
        line_numbers = added_line_numbers(catalog_diff(base_revision, catalog))
        selected, selected_problems = changed_entries(catalog, head_text, line_numbers)
        changed.extend(selected)
        problems.extend(new_validation_problems(base_catalog_entries, selected, selected_problems))

    problems.extend(new_duplicate_problems(base_entries, head_entries))
    for problem in sorted(set(problems), key=lambda item: (item.catalog, item.line, item.message)):
        print(problem.render())
    if problems:
        print(f"Catalog validation failed with {len(set(problems))} error(s).")
        return 1

    print(f"Catalog validation passed for {len(changed)} added or modified entr{'y' if len(changed) == 1 else 'ies'}.")
    if run_network:
        warnings = network_warnings(changed)
        for warning in warnings:
            print(warning.render("warning"))
        print(f"Advisory network checks completed with {len(warnings)} warning(s).")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-revision",
        default=os.environ.get("GITHUB_BASE_SHA"),
        help="Git revision to compare against (or set GITHUB_BASE_SHA)",
    )
    parser.add_argument("--network", action="store_true", help="run advisory checks for changed stream URLs")
    args = parser.parse_args(argv)
    if not args.base_revision:
        parser.error("--base-revision is required when GITHUB_BASE_SHA is not set")
    try:
        return run(args.base_revision, args.network)
    except (OSError, RuntimeError, UnicodeError) as error:
        print(f"Catalog validator could not run: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import concurrent.futures
import ipaddress
import socket
from typing import Sequence
import urllib.error
import urllib.parse
import urllib.request

from catalog import links_in
from models import STREAM_AVAILABILITY, Entry, Problem


USER_AGENT = "Catalog-Link-Validator/1.0"
NETWORK_TIMEOUT_SECONDS = 5
NETWORK_RESPONSE_LIMIT = 64 * 1024
NETWORK_URL_LIMIT = 20


def _public_addresses(hostname: str) -> tuple[bool, str | None]:
    if hostname.casefold() == "localhost" or hostname.casefold().endswith(".localhost"):
        return False, "local destinations are not probed"
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(hostname, None)}
    except OSError as error:
        return False, f"DNS lookup failed ({error.__class__.__name__})"
    for address in addresses:
        if not ipaddress.ip_address(address).is_global:
            return False, "private or non-global destinations are not probed"
    return True, None


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
                warnings.append(
                    Problem(entry.catalog, entry.line, STREAM_AVAILABILITY, f"advisory stream check: {message}")
                )
    if omitted and entries:
        warnings.append(
            Problem(
                entries[0].catalog,
                entries[0].line,
                STREAM_AVAILABILITY,
                f"advisory stream check skipped {omitted} URLs after the safety limit",
            )
        )
    return sorted(warnings, key=lambda item: (item.catalog, item.line, item.message))

import dataclasses
from pathlib import Path
import sys
import unittest
from unittest import mock
import urllib.error


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import catalog  # noqa: E402
import duplicates  # noqa: E402
import git_changes  # noqa: E402
from models import Entry  # noqa: E402
import network_checks  # noqa: E402


def television_row(
    name="Example TV",
    stream="[m3u8](https://media.example/live.m3u8)",
    web="[web](https://example.com/live)",
    logo="[logo](https://example.com/logo.png)",
    epg="-",
    info="-",
):
    return f"| {name} | {stream} | {web} | {logo} | {epg} | {info} |"


def entry(name="Example TV", stream="[m3u8](https://media.example/live.m3u8)", epg="-"):
    return Entry(
        "TELEVISION.md",
        7,
        "Nacionales",
        name,
        stream,
        "[web](https://example.com/live)",
        "[logo](https://example.com/logo.png)",
        epg,
        "-",
    )


class DiffTests(unittest.TestCase):
    def test_added_line_numbers_tracks_head_side_of_modification(self):
        diff = """@@ -5,2 +5,3 @@
 unchanged
-old
+new
+added
"""
        self.assertEqual({6, 7}, git_changes.added_line_numbers(diff))


class EntryValidationTests(unittest.TestCase):
    def test_valid_entry_supports_multiple_labeled_streams(self):
        item = entry(
            stream=(
                "[m3u8 # GEO # 1](https://media.example/one.m3u8) - "
                "[youtube # 2](https://www.youtube.com/channel/example/live)"
            )
        )
        self.assertEqual([], catalog.validate_entry(item))

    def test_stream_url_may_contain_balanced_parentheses(self):
        item = entry(stream="[m3u8](https://media.example/channel(europe)/live.m3u8)")
        self.assertEqual([], catalog.validate_entry(item))

    def test_rejects_bad_link_label_and_info_spacing(self):
        item = entry(stream="[video](https://media.example/live)")
        item = dataclasses.replace(item, info="GEO, EMB")
        messages = [problem.message for problem in catalog.validate_entry(item)]
        self.assertTrue(any("unsupported stream" in message for message in messages))
        self.assertTrue(any("Info must" in message for message in messages))

    def test_rejects_embedded_url_credentials(self):
        item = entry(stream="[m3u8](https://fake-user:fake-password@media.example/live.m3u8)")
        messages = [problem.message for problem in catalog.validate_entry(item)]
        self.assertTrue(any("embedded credentials" in message for message in messages))

    def test_changed_malformed_row_is_blocking(self):
        text = "\n".join(
            [
                "# Canales de Televisión",
                "",
                "## Nacionales",
                "",
                catalog.EXPECTED_HEADERS["TELEVISION.md"],
                "| - | - | - | - | - | - |",
                "| Broken | [m3u8](https://example.com/live.m3u8) | [web](https://example.com) | - | - |",
            ]
        )
        selected, problems = catalog.changed_entries("TELEVISION.md", text, {7})
        self.assertEqual([], selected)
        self.assertTrue(any("six" in problem.message for problem in problems))

    def test_unchanged_legacy_row_is_not_format_validated(self):
        text = "\n".join(
            [
                catalog.EXPECTED_HEADERS["TELEVISION.md"],
                "| - | - | - | - | - | - |",
                television_row(info=""),
                television_row(name="New TV"),
            ]
        )
        selected, problems = catalog.changed_entries("TELEVISION.md", text, {4})
        self.assertEqual(["New TV"], [item.name for item in selected])
        self.assertEqual([], problems)

    def test_changed_non_pipe_text_inside_table_is_blocking(self):
        text = "\n".join(
            [
                catalog.EXPECTED_HEADERS["TELEVISION.md"],
                "| - | - | - | - | - | - |",
                television_row(),
                "not a Markdown table row",
                television_row(name="Second TV"),
            ]
        )
        _, problems = catalog.changed_entries("TELEVISION.md", text, {4})
        self.assertTrue(any("start and end" in problem.message for problem in problems))

    def test_legacy_problem_is_grandfathered_while_field_is_unchanged(self):
        legacy = entry(stream="[video](https://media.example/live)")
        changed = dataclasses.replace(legacy, web="[web](https://example.com/new)")
        problems = catalog.validate_entry(changed)
        self.assertEqual([], catalog.new_validation_problems([legacy], [changed], problems))

    def test_new_problem_on_changed_field_is_blocking(self):
        base = entry()
        changed = dataclasses.replace(base, stream="[video](https://media.example/live)")
        problems = catalog.validate_entry(changed)
        self.assertTrue(catalog.new_validation_problems([base], [changed], problems))


class DuplicateTests(unittest.TestCase):
    def test_existing_duplicate_is_grandfathered(self):
        base = [entry("Same"), entry("Same")]
        head = [entry("Same"), entry("Same")]
        self.assertEqual([], duplicates.new_duplicate_problems(base, head))

    def test_increased_duplicate_count_is_blocking(self):
        base = [entry("Same")]
        head = [entry("Same"), entry("Same")]
        messages = [problem.message for problem in duplicates.new_duplicate_problems(base, head)]
        self.assertTrue(any("duplicate name" in message for message in messages))
        self.assertTrue(any("duplicate stream URL" in message for message in messages))

    def test_names_are_scoped_per_catalog(self):
        tv = entry("Shared name")
        radio = dataclasses.replace(
            tv,
            catalog="RADIO.md",
            stream="[mp3](https://radio.example/live.mp3)",
        )
        self.assertEqual([], duplicates.new_duplicate_problems([], [tv, radio]))


class NetworkTests(unittest.TestCase):
    def test_user_agent_is_generic(self):
        self.assertEqual("Catalog-Link-Validator/1.0", network_checks.USER_AGENT)

    @mock.patch.object(network_checks, "_public_addresses", return_value=(True, None))
    @mock.patch.object(network_checks, "_safe_urlopen")
    def test_network_failure_is_returned_as_warning_text(self, safe_urlopen, _public):
        safe_urlopen.side_effect = urllib.error.URLError("offline")
        message = network_checks.check_url("https://media.example/live.m3u8")
        self.assertIn("request failed", message)

    @mock.patch.object(network_checks.socket, "getaddrinfo")
    def test_private_destination_is_not_requested(self, getaddrinfo):
        getaddrinfo.return_value = [(None, None, None, None, ("127.0.0.1", 0))]
        safe, reason = network_checks._public_addresses("internal.example")
        self.assertFalse(safe)
        self.assertIn("non-global", reason)


if __name__ == "__main__":
    unittest.main()

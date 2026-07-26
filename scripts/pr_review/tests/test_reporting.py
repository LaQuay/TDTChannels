from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from models import LOGO_FORMAT, ROW_STRUCTURE, Problem  # noqa: E402
from reporting import build_report, render_summary, write_report  # noqa: E402


class ReportingTests(unittest.TestCase):
    def test_report_tracks_individual_failures_and_network_warnings(self):
        report = build_report(
            attempted={ROW_STRUCTURE, LOGO_FORMAT},
            problems=[Problem("TELEVISION.md", 7, LOGO_FORMAT, "bad logo")],
            changed_entries=1,
            network_ran=True,
            network_attempted=True,
            network_warnings=2,
        )
        self.assertEqual("passed", report["checks"][ROW_STRUCTURE]["status"])
        self.assertEqual("failed", report["checks"][LOGO_FORMAT]["status"])
        self.assertEqual("warnings", report["checks"]["stream_availability"]["status"])

    def test_summary_uses_contributor_facing_checks(self):
        report = build_report(
            attempted={ROW_STRUCTURE},
            problems=[],
            changed_entries=0,
            network_ran=False,
            network_attempted=False,
            network_warnings=0,
        )
        with tempfile.TemporaryDirectory() as directory:
            report_path = str(Path(directory) / "report.json")
            write_report(report_path, report)
            summary = render_summary(
                report_path,
                unit_tests="success",
                deterministic_validation="success",
                network_checks="skipped",
            )
        self.assertIn("| Table row structure | ✅ Passed | Yes |", summary)
        self.assertIn("| Logo link format | ➖ Not applicable | Yes |", summary)
        self.assertIn("Validator self-tests: ✅ Passed", summary)


if __name__ == "__main__":
    unittest.main()

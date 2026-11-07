import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from hw05.task3.log_analyzer import (
    count_logs_by_level,
    display_log_counts,
    display_log_details,
    filter_logs_by_level,
    load_logs,
    parse_log_line,
)
from hw05.task3.main import main

SAMPLE_LOG = """2024-01-22 08:30:01 INFO User logged in successfully.
2024-01-22 08:45:23 DEBUG Attempting to connect to the database.
2024-01-22 09:00:45 ERROR Database connection failed.
2024-01-22 09:15:10 INFO Data export completed.
2024-01-22 10:30:55 WARNING Disk usage above 80%.
2024-01-22 11:05:00 DEBUG Starting data backup process.
2024-01-22 11:30:15 ERROR Backup process failed.
2024-01-22 12:00:00 INFO User logged out.
2024-01-22 12:45:05 DEBUG Checking system health.
2024-01-22 13:30:30 INFO Scheduled maintenance.
"""


class LogFileTestCase(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._directory.cleanup)

    def write_log(self, content, name="test.log"):
        path = os.path.join(self._directory.name, name)
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return path


class TestParseLogLine(unittest.TestCase):
    def test_parses_all_components(self):
        line = "2024-01-22 09:00:45 ERROR Database connection failed."
        self.assertEqual(
            parse_log_line(line),
            {
                "date": "2024-01-22",
                "time": "09:00:45",
                "level": "ERROR",
                "message": "Database connection failed.",
            },
        )

    def test_message_may_contain_spaces_and_symbols(self):
        line = "2024-01-22 10:30:55 WARNING Disk usage above 80%."
        self.assertEqual(parse_log_line(line)["message"], "Disk usage above 80%.")

    def test_surrounding_whitespace_is_ignored(self):
        line = "  2024-01-22 08:30:01 INFO User logged in successfully.  \n"
        self.assertEqual(parse_log_line(line)["level"], "INFO")

    def test_blank_line_returns_empty_dict(self):
        self.assertEqual(parse_log_line("   "), {})

    def test_malformed_line_returns_empty_dict(self):
        self.assertEqual(parse_log_line("not a log line"), {})

    def test_missing_message_returns_empty_dict(self):
        self.assertEqual(parse_log_line("2024-01-22 08:30:01 INFO"), {})

    def test_lowercase_level_is_not_accepted(self):
        self.assertEqual(parse_log_line("2024-01-22 08:30:01 info message"), {})


class TestLoadLogs(LogFileTestCase):
    def test_loads_every_record(self):
        path = self.write_log(SAMPLE_LOG)
        self.assertEqual(len(load_logs(path)), 10)

    def test_skips_blank_and_malformed_lines(self):
        path = self.write_log(
            "2024-01-22 08:30:01 INFO ok\n\n   \ngarbage line\n2024-01-22 09:00:45 ERROR bad\n"
        )
        logs = load_logs(path)
        self.assertEqual([record["level"] for record in logs], ["INFO", "ERROR"])

    def test_empty_file_returns_empty_list(self):
        self.assertEqual(load_logs(self.write_log("")), [])

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_logs(os.path.join(self._directory.name, "nope.log"))


class TestFilterLogsByLevel(LogFileTestCase):
    def setUp(self):
        super().setUp()
        self.logs = load_logs(self.write_log(SAMPLE_LOG))

    def test_filters_by_level(self):
        errors = filter_logs_by_level(self.logs, "ERROR")
        self.assertEqual(
            [record["message"] for record in errors],
            ["Database connection failed.", "Backup process failed."],
        )

    def test_level_argument_is_case_insensitive(self):
        self.assertEqual(
            filter_logs_by_level(self.logs, "error"),
            filter_logs_by_level(self.logs, "ERROR"),
        )

    def test_unknown_level_returns_empty_list(self):
        self.assertEqual(filter_logs_by_level(self.logs, "TRACE"), [])

    def test_does_not_mutate_input(self):
        filter_logs_by_level(self.logs, "INFO")
        self.assertEqual(len(self.logs), 10)


class TestCountLogsByLevel(LogFileTestCase):
    def test_counts_sample_levels(self):
        logs = load_logs(self.write_log(SAMPLE_LOG))
        self.assertEqual(
            count_logs_by_level(logs),
            {"INFO": 4, "DEBUG": 3, "ERROR": 2, "WARNING": 1},
        )

    def test_empty_logs_return_empty_dict(self):
        self.assertEqual(count_logs_by_level([]), {})


class TestDisplayLogCounts(unittest.TestCase):
    def render(self, counts):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            display_log_counts(counts)
        return buffer.getvalue().splitlines()

    def test_header_and_rows(self):
        lines = self.render({"INFO": 4, "DEBUG": 3, "ERROR": 2, "WARNING": 1})
        self.assertEqual(lines[0], "Log level | Count")
        self.assertEqual(lines[1], "----------|----------")
        self.assertEqual(lines[2], "INFO      | 4")
        self.assertEqual(lines[5], "WARNING   | 1")

    def test_empty_counts_prints_only_header(self):
        self.assertEqual(len(self.render({})), 2)


class TestDisplayLogDetails(LogFileTestCase):
    def test_prints_date_time_and_message(self):
        logs = load_logs(self.write_log(SAMPLE_LOG))
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            display_log_details(filter_logs_by_level(logs, "error"), "error")
        lines = buffer.getvalue().splitlines()
        self.assertEqual(lines[1], "Log details for level 'ERROR':")
        self.assertEqual(lines[2], "2024-01-22 09:00:45 - Database connection failed.")
        self.assertEqual(lines[3], "2024-01-22 11:30:15 - Backup process failed.")

    def test_empty_logs_print_only_the_heading(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            display_log_details([], "error")
        self.assertEqual(buffer.getvalue(), "\nLog details for level 'ERROR':\n")


class TestMain(LogFileTestCase):
    def run_main(self, args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(args)
        return code, out.getvalue(), err.getvalue()

    def test_counts_only(self):
        path = self.write_log(SAMPLE_LOG)
        code, out, _ = self.run_main([path])
        self.assertEqual(code, 0)
        self.assertIn("INFO      | 4", out)
        self.assertNotIn("Log details", out)

    def test_counts_plus_details(self):
        path = self.write_log(SAMPLE_LOG)
        code, out, _ = self.run_main([path, "error"])
        self.assertEqual(code, 0)
        self.assertIn("Log details for level 'ERROR':", out)
        self.assertIn("2024-01-22 09:00:45 - Database connection failed.", out)

    def test_missing_file_reports_error(self):
        code, _, err = self.run_main([os.path.join(self._directory.name, "nope.log")])
        self.assertEqual(code, 1)
        self.assertIn("File not found", err)

    def test_directory_instead_of_file_reports_error(self):
        code, _, err = self.run_main([self._directory.name])
        self.assertEqual(code, 1)
        self.assertIn("not a directory", err)

    def test_unknown_level_reports_error(self):
        path = self.write_log(SAMPLE_LOG)
        code, _, err = self.run_main([path, "trace"])
        self.assertEqual(code, 1)
        self.assertIn("Unknown log level", err)

    def test_file_without_valid_records_reports_error(self):
        path = self.write_log("garbage\nmore garbage\n")
        code, _, err = self.run_main([path])
        self.assertEqual(code, 1)
        self.assertIn("No valid log records found", err)

    def test_no_arguments_shows_usage(self):
        code, _, err = self.run_main([])
        self.assertEqual(code, 2)
        self.assertIn("Usage", err)

    def test_too_many_arguments_shows_usage(self):
        code, _, err = self.run_main(["a", "b", "c"])
        self.assertEqual(code, 2)
        self.assertIn("Usage", err)


if __name__ == "__main__":
    unittest.main()

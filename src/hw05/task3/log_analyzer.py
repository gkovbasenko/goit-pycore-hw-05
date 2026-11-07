import re
from collections import Counter
from pathlib import Path

LOG_LINE_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+"
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Z]+)\s+"
    r"(?P<message>.+)$"
)


def parse_log_line(line: str) -> dict:
    """Split one log line into date/time/level/message; empty dict if malformed."""
    match = LOG_LINE_PATTERN.match(line.strip())
    return match.groupdict() if match else {}


def load_logs(file_path: str) -> list:
    with Path(file_path).open(encoding="utf-8") as file:
        return [record for line in file if (record := parse_log_line(line))]


def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda record: record["level"] == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(record["level"] for record in logs))


def display_log_counts(counts: dict) -> None:
    header = "Log level"
    width = max(len(header), *(len(level) for level in counts)) if counts else len(header)
    print(f"{header:<{width}} | Count")
    print(f"{'-' * width}-|----------")
    for level, count in counts.items():
        print(f"{level:<{width}} | {count}")


def display_log_details(logs: list, level: str) -> None:
    print(f"\nLog details for level '{level.upper()}':")
    for record in logs:
        print(f"{record['date']} {record['time']} - {record['message']}")

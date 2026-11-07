import sys

from hw05.task3.log_analyzer import (
    count_logs_by_level,
    display_log_counts,
    display_log_details,
    filter_logs_by_level,
    load_logs,
)

KNOWN_LEVELS = {"INFO", "ERROR", "DEBUG", "WARNING"}


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not 1 <= len(args) <= 2:
        print("Usage: python -m hw05.task3 <log_file> [level]", file=sys.stderr)
        return 2

    file_path, level = args[0], args[1] if len(args) == 2 else None

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
        return 1
    except IsADirectoryError:
        print(f"Expected a file, not a directory: {file_path}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"Permission denied: {file_path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"Could not decode file as UTF-8: {file_path}", file=sys.stderr)
        return 1

    if not logs:
        print(f"No valid log records found in: {file_path}", file=sys.stderr)
        return 1

    display_log_counts(count_logs_by_level(logs))

    if level is not None:
        if level.upper() not in KNOWN_LEVELS:
            print(f"\nUnknown log level: {level}", file=sys.stderr)
            return 1
        display_log_details(filter_logs_by_level(logs, level), level)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

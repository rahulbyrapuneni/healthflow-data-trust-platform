from pathlib import Path

from src.frontend.views.audit_logs import parse_log_file


def test_parse_log_file_reads_valid_log_line(
    tmp_path: Path,
):
    log_file = tmp_path / "api.log"

    log_file.write_text(
        (
            "2026-08-04 18:15:00 | INFO     | "
            "healthflow.api  | Request completed\n"
        ),
        encoding="utf-8",
    )

    rows = parse_log_file(
        component="API",
        file_path=log_file,
    )

    assert len(rows) == 1
    assert rows[0]["component"] == "API"
    assert rows[0]["level"] == "INFO"
    assert rows[0]["message"] == "Request completed"


def test_parse_log_file_skips_invalid_lines(
    tmp_path: Path,
):
    log_file = tmp_path / "quality.log"

    log_file.write_text(
        "This is not a valid log line\n",
        encoding="utf-8",
    )

    rows = parse_log_file(
        component="Quality",
        file_path=log_file,
    )

    assert rows == []


def test_missing_log_file_returns_empty(
    tmp_path: Path,
):
    rows = parse_log_file(
        component="Pipeline",
        file_path=tmp_path / "missing.log",
    )

    assert rows == []
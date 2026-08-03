from src.quality.run_metadata import create_run_metadata


def test_run_metadata_contains_unique_id():
    first_run = create_run_metadata()
    second_run = create_run_metadata()

    assert first_run.run_id
    assert second_run.run_id
    assert first_run.run_id != second_run.run_id


def test_run_metadata_contains_timestamp():
    run = create_run_metadata()

    assert run.run_timestamp
    assert "T" in run.run_timestamp
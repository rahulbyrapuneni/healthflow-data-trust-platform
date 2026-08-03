from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass
class RunMetadata:
    """Information that identifies one quality-check execution."""

    run_id: str
    run_timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)


def create_run_metadata() -> RunMetadata:
    """Create a unique identifier and UTC timestamp for a run."""

    return RunMetadata(
        run_id=str(uuid4()),
        run_timestamp=datetime.now(UTC).isoformat(),
    )
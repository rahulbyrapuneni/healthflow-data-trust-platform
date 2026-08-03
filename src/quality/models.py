from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Issue:
    """Represents one detected data-quality issue."""

    dataset: str
    record_id: Any
    field: str
    rule: str
    severity: str
    message: str
    category: str = "Data Quality"
    source_system: str = "Unknown"
    business_impact: str = "May reduce confidence in reporting."
    recommendation: str = "Review and correct the source record."

    def to_dict(self) -> dict:
        """Convert the issue into a dictionary."""

        return asdict(self)
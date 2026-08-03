from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class APIResponse:
    """Represents a downloaded API response."""

    source: str

    endpoint: str

    row_count: int

    success: bool

    status_code: int

    message: str
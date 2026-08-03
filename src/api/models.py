from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class APIResponse:
    """Represents one response returned by an external API."""

    source: str
    endpoint: str
    success: bool
    status_code: int
    row_count: int
    message: str
    data: Any
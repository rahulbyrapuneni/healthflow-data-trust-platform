from zoneinfo import ZoneInfo
import pandas as pd

DEFAULT_TIMEZONE = ZoneInfo("America/New_York")


def format_timestamp(
    timestamp: object,
    timezone=DEFAULT_TIMEZONE,
) -> str:
    """Format a UTC timestamp in US Eastern Time."""

    parsed = pd.to_datetime(
        timestamp,
        utc=True,
        errors="coerce",
    )

    if pd.isna(parsed):
        return "Not available"

    return (
        parsed.tz_convert(timezone)
        .strftime("%b %d, %Y • %I:%M %p %Z")
    )
class APIClientError(Exception):
    """Base exception for API client errors."""


class APIConnectionError(APIClientError):
    """Raised when the API cannot be reached."""


class APIRateLimitError(APIClientError):
    """Raised when an API rate limit is reached."""


class APIResponseError(APIClientError):
    """Raised when an API returns an unexpected response."""
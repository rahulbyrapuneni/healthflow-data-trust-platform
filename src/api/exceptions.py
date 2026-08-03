class APIClientError(Exception):
    """Base exception for all HealthFlow API-client errors."""


class APIConnectionError(APIClientError):
    """Raised when an external API cannot be reached."""


class APITimeoutError(APIClientError):
    """Raised when an API request exceeds its allowed time."""


class APIRateLimitError(APIClientError):
    """Raised when an API rate limit has been reached."""


class APIResponseError(APIClientError):
    """Raised when an API returns an unsuccessful response."""


class APIDataFormatError(APIClientError):
    """Raised when an API response cannot be parsed as expected."""
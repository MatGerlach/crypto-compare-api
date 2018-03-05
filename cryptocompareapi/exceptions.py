"""Exceptions used in the library."""


class HttpError(Exception):
    """A HTTP Error occured and needs to be handled."""


class TimeoutException(Exception):
    """In case of a Sever timeout."""


class CryptoCompareError(Exception):
    """The API request resulted in a Error."""

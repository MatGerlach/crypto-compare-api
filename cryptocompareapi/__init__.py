"""An API package for the public CryptoCompare API."""
from .wrapper import CryptoCompare
from .wrapper import CryptoCompareMethod
from .wrapper import HttpError
from .wrapper import TimeoutException
from .wrapper import CryptoCompareError
__all__ = ['wrapper']

"""Contains Enumerations containing information about API-methods."""
from enum import Enum

BASE_URL = "https://min-api.cryptocompare.com/data/"


class RateLimitGroup(Enum):
    """Enumeration of the different Rate limit groups.

    All Methods in one group share one rate limit
    """

    HISTO = 1,
    PRICE = 2,
    NEWS = 3,
    STRICT = 4
    NO = 5


class CryptoCompareMethod(Enum):
    """Enumeration of methods defined by API, holding static information.

    Use full_url property to get the full url
    """

    PRICE = ("price", 10, RateLimitGroup.PRICE)
    PRICE_MULT = ("pricemulti", 10, RateLimitGroup.PRICE)
    PRICE_MULTI_FULL = ("pricemultifull", 10, RateLimitGroup.PRICE)
    GENERATE_AVERAGE = ("generateAvg", 10, RateLimitGroup.PRICE)
    HISTO_DAY = ("histoday", 610, RateLimitGroup.HISTO)
    HISTO_HOUR = ("histohour", 610, RateLimitGroup.HISTO)
    HISTO_MINUTE = ("histominute", 40, RateLimitGroup.HISTO)
    HISTO_DAY_TIMESTAMP = ("pricehistorical", 86400, RateLimitGroup.HISTO)
    HISTO_DAY_AVERAGE = ("dayAvg", 610, RateLimitGroup.HISTO)
    TOP_EXCHANGES = ("top/exchanges", 120, RateLimitGroup.PRICE)
    TOP_EXCHANGES_FULL = ("top/exchange/full", 120, RateLimitGroup.PRICE)
    TOP_VOLUMES = ("top/volumes", 120, RateLimitGroup.PRICE)
    TOP_PAIRS = ("top/pairs", 120, RateLimitGroup.PRICE)
    TOP_COINS = ("top/totalvol", 120, RateLimitGroup.PRICE)
    SUBS_WATCHLIST = ("subsWatchlist", 60, RateLimitGroup.PRICE)
    SUBS_BY_PAIR = ("subs", 10, RateLimitGroup.PRICE)
    LIST_NEWS_PROVIDER = ("news/providers", 120, RateLimitGroup.NEWS)
    LATEST_NEWS_ARTICLES = ("news/", 120, RateLimitGroup.NEWS)
    LIST_EXCHANGES = ("all/exchanges", 60, RateLimitGroup.PRICE)
    LIST_COINS = ("all/coinlist", 60, RateLimitGroup.PRICE)
    RATE_LIMIT = ("stats/rate/limit", 1, RateLimitGroup.NO)

    def __init__(self, rel_url, caching, rateLimitGroup):
        """Enum constructor."""
        self.rel_url = rel_url
        self.caching = caching
        self.rateLimitGroup = rateLimitGroup

    @property
    def full_url(self):
        """Get the full url to the API-method."""
        return BASE_URL + self.rel_url

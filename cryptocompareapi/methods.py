"""Contains Enumerations containing information about API-methods."""
from enum import Enum


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

    PRICE = (
        "https://min-api.cryptocompare.com/data/price",
        10, RateLimitGroup.PRICE)
    PRICE_MULT = (
        "https://min-api.cryptocompare.com/data/pricemulti",
        10, RateLimitGroup.PRICE)
    PRICE_MULTI_FULL = (
        "https://min-api.cryptocompare.com/data/pricemultifull",
        10, RateLimitGroup.PRICE)
    GENERATE_AVERAGE = (
        "https://min-api.cryptocompare.com/data/generateAvg",
        10, RateLimitGroup.PRICE)
    HISTO_DAY = (
        "https://min-api.cryptocompare.com/data/histoday",
        610, RateLimitGroup.HISTO)
    HISTO_HOUR = (
        "https://min-api.cryptocompare.com/data/histohour",
        610, RateLimitGroup.HISTO)
    HISTO_MINUTE = (
        "https://min-api.cryptocompare.com/data/histominute",
        40, RateLimitGroup.HISTO)
    HISTO_DAY_TIMESTAMP = (
        "https://min-api.cryptocompare.com/data/pricehistorical",
        86400, RateLimitGroup.HISTO)
    HISTO_DAY_AVERAGE = (
        "https://min-api.cryptocompare.com/data/dayAvg",
        610, RateLimitGroup.HISTO)
    TOP_EXCHANGES = (
        "https://min-api.cryptocompare.com/data/top/exchanges",
        120, RateLimitGroup.PRICE)
    TOP_EXCHANGES_FULL = (
        "https://min-api.cryptocompare.com/data/top/exchange/full",
        120, RateLimitGroup.PRICE)
    TOP_VOLUMES = (
        "https://min-api.cryptocompare.com/data/top/volumes",
        120, RateLimitGroup.PRICE)
    TOP_PAIRS = (
        "https://min-api.cryptocompare.com/data/top/pairs",
        120, RateLimitGroup.PRICE)
    TOP_COINS = (
        "https://min-api.cryptocompare.com/data/top/totalvol",
        120, RateLimitGroup.PRICE)
    SUBS_WATCHLIST = (
        "https://min-api.cryptocompare.com/data/subsWatchlist",
        60, RateLimitGroup.PRICE)
    SUBS_BY_PAIR = (
        "https://min-api.cryptocompare.com/data/subs",
        10, RateLimitGroup.PRICE)
    LIST_NEWS_PROVIDER = (
        "https://min-api.cryptocompare.com/data/news/providers",
        120, RateLimitGroup.NEWS)
    LATEST_NEWS_ARTICLES = (
        "https://min-api.cryptocompare.com/data/news/",
        120, RateLimitGroup.NEWS)
    LIST_EXCHANGES = (
        "https://min-api.cryptocompare.com/data/all/exchanges",
        60, RateLimitGroup.PRICE)
    LIST_COINS = (
        "https://min-api.cryptocompare.com/data/all/coinlist",
        60, RateLimitGroup.PRICE)
    RATE_LIMIT = (
        "https://min-api.cryptocompare.com/stats/rate/limit",
        1, RateLimitGroup.NO)

    def __init__(self, full_url, caching, rateLimitGroup):
        """Enum constructor."""
        self.full_url = full_url
        self.caching = caching
        self.rateLimitGroup = rateLimitGroup

    @property
    def full_url(self):
        """Get the full url to the API-method."""
        return self.full_url

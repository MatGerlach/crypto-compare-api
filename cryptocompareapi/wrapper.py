"""A wrapper for the CryptoCompare API.

TODO:
    - The length of lists in parameters is limited by the API, check if API
      returns an error message for to long param, else check in code
    - Test
    - Implement a cache based on the caching times of the API
    - Count the requests per Group in a time period
    - Additional Errors necessary?
"""
import requests
import os
from enum import Enum

from .exceptions import HttpError, TimeoutException, CryptoCompareError
from .methods import CryptoCompareMethod

DEFAULT_EXCHANGE = "CCCAGG"
DEFAULT_TIMEOUT = 5.0  # In seconds


class CalculationType(Enum):
    """Parameter Values for Calculation Type."""

    CLOSE = "Close",  # a Close of the day close price,
    MID_HIGH_LOW = "MidHighLow",  # the average between the 24 H high/low
    VO_IF_VO_IT = "VoIFVoIT"  # the total volume to / the total volume from


def _create_param_list_string(object):
    """Create a list parameter as specified in API-Doc."""
    if isinstance(object, str):
        lst = [object]
    elif isinstance(object, list):
        lst = object
    else:
        lst = [object]
    return ",".join(lst)


class CryptoCompare(object):
    """Wrapper around the Crypto-Compare-API.

    The Object offers the methods as specified on:
    https://min-api.cryptocompare.com/

    Please consult the API documentation for further information.

    The methods may raise different types of Exceptions that should be catched:
        - HTTPError: in case the HTTP-request failed with a status != 200
        - TimeoutException: in case the connection to API timed out
        - CryptoCompareError: in case the API returned an error message
    """

    def __init__(self, appName, timeout=DEFAULT_TIMEOUT):
        """Create an instance.

        Args:
            appName (str): Name of your application, is send with every
                request
            timeout (dbl): Seconds to wait for a server response. Default 5s
        """
        self.appName = appName
        self.timeout = timeout

    def single_symbol_price(self, from_symbol, to_symbols,
                            exchange=DEFAULT_EXCHANGE, try_conversion=True):
        """Get the current price of a cryptocurrency.

        Args:
            from_symbols(str): The symbol to get the price for
            to_symbols (list<str>): the symbols to convert into
            tryConversion(bool): If set to false, it will try to get only
                    direct trading values(Default true)
            exchange(str): The exchange to obtain data from (Default "CCCAGG")

        Returns:
            { <to_symbol_1> : <value_1>,
            ...
             <to_symbol_n>: <value_n> }

        Raises:
            HttpError: The Request failed due to a HTTPError, should always be
                handled
            TimeoutException: The Request timed out
            CryptoCompareError: The API returned an error message

        """
        params = {}
        params["fsym"] = from_symbol
        params["tsyms"] = _create_param_list_string(to_symbols)
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        return self._try_get_request(
            CryptoCompareMethod.PRICE, params)

    def multiple_symbols_price(self, from_symbols, to_symbols,
                               exchange=DEFAULT_EXCHANGE, try_conversion=True):
        """Get the current price of one or more cryptocurrencies.

        Args:
            from_symbols (list<str>): The symbols to get the price for
            to_symbols (list<str>): the symbols to convert into
            tryConversion(bool): If set to false, it will try to get only
                direct trading values(Default true)
            exchange(str): The exchange to obtain data from (Default "CCCAGG")

        Returns:
            {
              <from_symbol_1> : {
                <to_symbol_1>: <value_1> ,
                ...
                <to_symbol_n> : <value_n>
              }
              ...
              <from_symbol_m> : {
                <to_symbol_1>: <value_1> ,
                ...
                <to_symbol_n> : <value_n>
              }
            }

        Raises:
            HttpError: The Request failed due to a HTTPError, should always be
                handled
            TimeoutException: The Request timed out
            CryptoCompareError: The API returned an error message

        """
        params = {}
        params["fsyms"] = _create_param_list_string(from_symbols)
        params["tsyms"] = _create_param_list_string(to_symbols)
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        return self._try_get_request(CryptoCompareMethod.PRICE_MULT, params)

    def multiple_symbols_full_data(self, from_symbols, to_symbols,
                                   exchange=DEFAULT_EXCHANGE,
                                   try_conversion=True):
        """Get all the current trading info (price, vol, open, high, low etc).

        Args:
            from_symbols (list<str>): The symbols to get the price for
            to_symbols (list<str>): the symbols to convert into
            tryConversion(bool): If set to false, it will try to get only
                direct trading values(Default True)
            exchange(str): The exchange to obtain data from (Default "CCCAGG")

        Returns:
            An dictionary with the structure:
            {
                "RAW": {
                    <from_symbol_1>:{...},
                    ...
                    <from_symbol_n>:{...},
                },
                "DISPLAY": {
                    <from_symbol_1>:{...},
                    ...
                    <from_symbol_n>:{...},
                }
            }

        Raises:
            HttpError: The Request failed due to a HTTPError, should always be
                handled
            TimeoutException: The Request timed out
            CryptoCompareError: The API returned an error message

        """
        # Make single symbols to a singleton list
        params = {}
        params["fsyms"] = _create_param_list_string(from_symbols)
        params["tsyms"] = _create_param_list_string(to_symbols)
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        return self._try_get_request(
            CryptoCompareMethod.PRICE_MULTI_FULL, params)

    def generate_custom_average(self, from_symbol, to_symbol,
                                exchange=DEFAULT_EXCHANGE):
        """Compute the current trading info as a volume weighted average.

        Args:
            from_symbols (list<str>): The symbols to get the price for
            to_symbols (list<str>): the symbols to convert into
            exchange(str): The exchange to obtain data from (Default "CCCAGG")

        Returns:
            An dictionary with the structure:
            {
                "RAW": {
                    <from_symbol_1>:{...},
                    ...
                    <from_symbol_n>:{...},
                },
                "DISPLAY": {
                    <from_symbol_1>:{...},
                    ...
                    <from_symbol_n>:{...},
                }
            }

        Raises:
            HttpError: The Request failed due to a HTTPError, should always be
                handled
            TimeoutException: The Request timed out
            CryptoCompareError: The API returned an error message

        """
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["e"] = exchange
        return self._try_get_request(
            CryptoCompareMethod.GENERATE_AVERAGE, params)

    def historical_daily(self, from_symbol, to_symbol,
                         exchange=DEFAULT_EXCHANGE,
                         try_conversion=True,
                         aggregate=1,
                         limit=31,
                         allData=False,
                         toTimestamp=None):
        """Get close, high, ..- from the daily historical data."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        params["aggregate"] = aggregate
        params["limit"] = limit
        if allData:
            params["allData"] = allData
        if toTimestamp is not None:
            params["toTs"] = toTimestamp
        return self._try_get_request(CryptoCompareMethod.HISTO_DAY, params)

    def historical_hourly(self, from_symbol, to_symbol,
                          exchange=DEFAULT_EXCHANGE,
                          try_conversion=True,
                          aggregate=1,
                          limit=170,
                          toTimestamp=None):
        """Get close, high, ... from the houry historical data."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        params["aggregate"] = aggregate
        params["limit"] = limit
        if toTimestamp is not None:
            params["toTs"] = toTimestamp
        return self._try_get_request(CryptoCompareMethod.HISTO_HOUR, params)

    def historical_minute(self, from_symbol, to_symbol,
                          exchange=DEFAULT_EXCHANGE,
                          try_conversion=True,
                          aggregate=1,
                          limit=170,
                          toTimestamp=None):
        """Get close, high, ... from the minute historical data."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        params["aggregate"] = aggregate
        params["limit"] = limit
        if toTimestamp is not None:
            params["toTs"] = toTimestamp
        return self._try_get_request(CryptoCompareMethod.HISTO_MINUTE, params)

    def historical_day_timestamp(self, from_symbol, to_symbol,
                                 timestamp=None,
                                 exchange=DEFAULT_EXCHANGE,
                                 try_conversion=True,
                                 calculation_type=CalculationType.CLOSE):
        """Get the price of a cryptocurrency a given timestamp."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        params["calculationType"] = calculation_type
        if timestamp is not None:
            params["ts"] = timestamp
        return self._try_get_request(
            CryptoCompareMethod.HISTO_DAY_TIMESTAMP, params)

    def historical_day_average(self, from_symbol, to_symbol,
                               to_timestamp=None,
                               exchange=DEFAULT_EXCHANGE,
                               try_conversion=True,
                               avg_type=CalculationType.CLOSE,
                               utc_hour_diff=0):
        """Get day average price."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["e"] = exchange
        params["tryConversion"] = try_conversion
        params["avgType"] = avg_type
        params["UTCHourDiff"] = utc_hour_diff
        if to_timestamp is not None:
            params["toTs"] = to_timestamp
        return self._try_get_request(
            CryptoCompareMethod.HISTO_DAY_AVERAGE, params)

    def top_exchanges_volume(self, from_symbol, to_symbol, limit=5):
        """Get top exchanges by volume for a currency pair."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["limit"] = limit
        return self._try_get_request(CryptoCompareMethod.TOP_EXCHANGES, params)

    def top_exchange_full(self, from_symbol, to_symbol, limit=5):
        """Get top exchanges by volume for a pair plus the full CCCAGG data."""
        params = {}
        params["fsym"] = from_symbol
        params["tsym"] = to_symbol
        params["limit"] = limit
        return self._try_get_request(CryptoCompareMethod.TOP_EXCHANGES_FULL,
                                     params)

    def top_volumes(self, to_symbol, limit=21):
        """Get top coins by volume for the to currency."""
        params = {}
        params["tsym"] = to_symbol
        params["limit"] = limit
        return self._try_get_request(CryptoCompareMethod.TOP_VOLUMES, params)

    def top_pairs(self, from_symbol, limit=5):
        """Get top pairs by volume for a currency."""
        params = {}
        params["fsym"] = from_symbol
        params["limit"] = limit
        return self._try_get_request(CryptoCompareMethod.TOP_PAIRS, params)

    def top_total_volume(self, to_symbol, limit=10, page=1):
        """Get a number of top coins by their total volume."""
        params = {}
        params["tsym"] = to_symbol
        params["limit"] = limit
        params["page"] = page
        return self._try_get_request(CryptoCompareMethod.TOP_COINS, params)

    def subs_watchlist(self, from_symbols, to_symbol):
        """Get combinations of subs and pricing info."""
        params = {}
        params["fsyms"] = _create_param_list_string(from_symbols)
        params["tsym"] = to_symbol
        return self._try_get_request(CryptoCompareMethod.SUBS_WATCHLIST,
                                     params)

    def subs_by_pair(self, from_symbol, to_symbols=None):
        """Get all the available streamer subscription channels for pairs."""
        params = {}
        params["fsym"] = from_symbol
        if to_symbols is not None:
            params["tsyms"] = _create_param_list_string(to_symbols)
        return self._try_get_request(CryptoCompareMethod.SUBS_BY_PAIR, params)

    def list_news_provider(self):
        """Return all the news providers CryptoCompare has integrated."""
        return self._try_get_request(CryptoCompareMethod.LIST_NEWS_PROVIDER,
                                     {})

    def latest_news_articles(self, feeds=None, last_timestamp=None, lang="EN"):
        """Return news articles from providers CryptoCompare has integrated."""
        params = {}
        params["lang"] = lang
        if feeds is not None:
            params["feeds"] = _create_param_list_string(feeds)
        if last_timestamp is not None:
            params["lTs"] = last_timestamp
        return self._try_get_request(CryptoCompareMethod.LATEST_NEWS_ARTICLES,
                                     params)

    def list_exchanges(self):
        """Return all the exchanges that CryptoCompare has integrated."""
        return self._try_get_request(CryptoCompareMethod.LIST_EXCHANGES, {})

    def list_coins(self):
        """Return all the coins that CryptoCompare added to the website."""
        return self._try_get_request(CryptoCompareMethod.LIST_COINS, {})

    def rate_limits(self):
        """Get the rate limits left for you."""
        return self._try_get_request(CryptoCompareMethod.RATE_LIMIT, {})

    def _try_get_request(self, method, params):
        """Try to perform a get request.

        Used to access used HTTP library just in one place

        Args:
            methdo (CryptoCompareMethod) : The requested Method
            params (dict<str>) : A dictionary of params to send with request

        Returns:
            The json-object inside the Response

        Raises:
            HttpError: The Request failed due to a HTTPError, should always be
                handled
            TimeoutException: The Request timed out
            CryptoCompareError: The API returned an error message

        """
        params["extraParams"] = self.appName
        try:
            response = requests.get(method.full_url, params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HttpError() from e
        except requests.exceptions.Timeout as e:
            raise TimeoutException() from e

        json = response.json()
        if "Response" in json and json["Response"] == "Error":
            raise CryptoCompareError(json["Message"])
        return json

from __future__ import annotations
from typing import Any, Dict, List, Optional
import finnhub
from utils.env_config import EnvConfig


class FinnhubAPIError(Exception):
    """Raised when a Finnhub API call fails or returns unexpected data."""

    def __init__(self, method: str, detail: str):
        self.method = method
        self.detail = detail
        super().__init__(f"[FinnhubAPIError] {method}() → {detail}")


class FinnhubClient:
    def __init__(self):
        self._client = finnhub.Client(api_key=EnvConfig.finnhub_key())

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    @staticmethod
    def _require(method: str, data: Any) -> Any:
        """
        Args:
            method: Method name, used in the error message.
            data:   Response from finnhub.Client.
        Returns:
            data unchanged when truthy.
        Raises:
            FinnhubAPIError: When data is None, empty dict, or empty list.
        """
        if data is None or data == {} or data == []:
            raise FinnhubAPIError(method, "empty response — check symbol or API key")
        return data

    # ------------------------------------------------------------------
    # Quote & Price
    # ------------------------------------------------------------------

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Real-time quote for a symbol.

        Args:
            symbol: Ticker symbol, e.g. "AAPL".

        Returns:
            {
                "c":  current price,
                "h":  day high,
                "l":  day low,
                "o":  open price,
                "pc": previous close,
                "t":  unix timestamp,
            }
        """
        try:
            data = self._client.quote(symbol)
            return self._require("get_quote", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_quote", str(exc)) from exc

    # ------------------------------------------------------------------
    # Company
    # ------------------------------------------------------------------

    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Company profile (name, exchange, logo, market cap, etc.).

        Args:
            symbol: Ticker symbol.

        Returns:
            Dict with company metadata fields.
        """
        try:
            data = self._client.company_profile2(symbol=symbol)
            return self._require("get_company_profile", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_company_profile", str(exc)) from exc

    def get_peers(self, symbol: str) -> List[str]:
        """
        List of peer ticker symbols for a given company.

        Args:
            symbol: Ticker symbol.

        Returns:
            List of peer ticker strings.
        """
        try:
            data = self._client.company_peers(symbol)
            return self._require("get_peers", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_peers", str(exc)) from exc

    # ------------------------------------------------------------------
    # News
    # ------------------------------------------------------------------

    def get_company_news(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
    ) -> List[Dict[str, Any]]:
        """
        Company-specific news articles.

        Args:
            symbol:    Ticker symbol.
            from_date: Start date string "YYYY-MM-DD".
            to_date:   End date string "YYYY-MM-DD".

        Returns:
            List of news article dicts (headline, source, url, datetime, etc.).
        """
        try:
            data = self._client.company_news(symbol, _from=from_date, to=to_date)
            return self._require("get_company_news", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_company_news", str(exc)) from exc

    def get_market_news(self, category: str = "general") -> List[Dict[str, Any]]:
        """
        General market news.

        Args:
            category: One of "general", "forex", "crypto", "merger".

        Returns:
            List of news article dicts.
        """
        try:
            data = self._client.general_news(category, min_id=0)
            return self._require("get_market_news", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_market_news", str(exc)) from exc

    # ------------------------------------------------------------------
    # Calendars
    # ------------------------------------------------------------------

    def get_earnings_calendar(
        self,
        from_date: str,
        to_date: str,
        symbol: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Earnings calendar for a date range.

        Args:
            from_date: Start date "YYYY-MM-DD".
            to_date:   End date "YYYY-MM-DD".
            symbol:    Optional ticker to filter results.

        Returns:
            Dict containing list of earnings events.
        """
        try:
            data = self._client.earnings_calendar(
                _from=from_date, to=to_date, symbol=symbol or "", international=False
            )
            return self._require("get_earnings_calendar", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_earnings_calendar", str(exc)) from exc

    def get_ipo_calendar(self, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        IPO calendar for a date range.

        Args:
            from_date: Start date "YYYY-MM-DD".
            to_date:   End date "YYYY-MM-DD".

        Returns:
            Dict containing list of IPO events.
        """
        try:
            data = self._client.ipo_calendar(_from=from_date, to=to_date)
            return self._require("get_ipo_calendar", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_ipo_calendar", str(exc)) from exc

    def get_economic_calendar(self) -> Dict[str, Any]:
        """
        Upcoming economic events / indicators.

        Returns:
            Dict containing list of economic calendar events.
        """
        try:
            data = self._client.economic_calendar()
            return self._require("get_economic_calendar", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_economic_calendar", str(exc)) from exc

    # ------------------------------------------------------------------
    # Fundamentals
    # ------------------------------------------------------------------

    def get_recommendation_trends(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Analyst buy/hold/sell recommendation trends.

        Args:
            symbol: Ticker symbol.

        Returns:
            List of monthly recommendation trend dicts.
        """
        try:
            data = self._client.recommendation_trends(symbol)
            return self._require("get_recommendation_trends", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_recommendation_trends", str(exc)) from exc

    def get_earnings_surprises(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Historical EPS surprises vs analyst estimates.

        Args:
            symbol: Ticker symbol.

        Returns:
            List of earnings surprise dicts (actual, estimate, period, surprise).
        """
        try:
            data = self._client.company_earnings(symbol, limit=4)
            return self._require("get_earnings_surprises", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_earnings_surprises", str(exc)) from exc

    def get_splits(self, symbol: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """
        Stock split history for a date range.

        Args:
            symbol:    Ticker symbol.
            from_date: Start date "YYYY-MM-DD".
            to_date:   End date "YYYY-MM-DD".

        Returns:
            Dict containing list of split events.
        """
        try:
            data = self._client.stock_splits(symbol, _from=from_date, to=to_date)
            return self._require("get_splits", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_splits", str(exc)) from exc

    def get_dividends(self, symbol: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Dividend history for a date range.

        Args:
            symbol:    Ticker symbol.
            from_date: Start date "YYYY-MM-DD".
            to_date:   End date "YYYY-MM-DD".

        Returns:
            List of dividend event dicts.
        """
        try:
            data = self._client.stock_dividends(symbol, _from=from_date, to=to_date)
            return self._require("get_dividends", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_dividends", str(exc)) from exc

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def get_search(self, query: str) -> Dict[str, Any]:
        """
        Symbol / company search.

        Args:
            query: Free-text search string.

        Returns:
            Dict with "count" and "result" list of matching symbols.
        """
        try:
            data = self._client.symbol_search(query)
            return self._require("get_search", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_search", str(exc)) from exc

    # ------------------------------------------------------------------
    # Technical Analysis
    # ------------------------------------------------------------------

    def get_technical_indicators(
        self,
        symbol: str,
        resolution: str = "D",
        indicator: str = "ema",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Technical indicator values (EMA, SMA, RSI, MACD, etc.).

        Args:
            symbol:     Ticker symbol.
            resolution: Bar resolution — 1, 5, 15, 30, 60, D, W, M.
            indicator:  Indicator name (ema, sma, rsi, macd, …).
            **kwargs:   Extra params forwarded to the API
                        (e.g. from_ts=1609459200, to_ts=1612137600, timeperiod=20).

        Returns:
            Dict with indicator values and metadata.
        """
        try:
            data = self._client.technical_indicator(
                symbol=symbol,
                resolution=resolution,
                _from=kwargs.pop("from_ts", 0),
                to=kwargs.pop("to_ts", 9_999_999_999),
                indicator=indicator,
                indicator_fields=kwargs or {},
            )
            return self._require("get_technical_indicators", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_technical_indicators", str(exc)) from exc

    def get_pattern_recognition(
        self, symbol: str, resolution: str = "D"
    ) -> Dict[str, Any]:
        """
        Candlestick pattern recognition.

        Args:
            symbol:     Ticker symbol.
            resolution: Bar resolution — 1, 5, 15, 30, 60, D, W, M.

        Returns:
            Dict with recognised pattern data.
        """
        try:
            data = self._client.pattern_recognition(symbol, resolution)
            return self._require("get_pattern_recognition", data)
        except FinnhubAPIError:
            raise
        except Exception as exc:
            raise FinnhubAPIError("get_pattern_recognition", str(exc)) from exc
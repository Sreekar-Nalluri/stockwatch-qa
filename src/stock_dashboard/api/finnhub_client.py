from __future__ import annotations
from typing import Any, Dict
import finnhub
from utils.env_config import EnvConfig


class FinnhubAPIError(Exception):
    def __init__(self, method: str, detail: str):
        self.method = method
        self.detail = detail
        super().__init__(f"[FinnhubAPIError] {method}() → {detail}")


class FinnhubClient:
    def __init__(self):
        self._client = finnhub.Client(api_key=EnvConfig.finnhub_key())

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

    # ------------------------------------------------------------------
    # Company Profile Assertions
    # ------------------------------------------------------------------

    @staticmethod
    def verify_company_profile_valid(response: Dict[str, Any]) -> None:
        assert response is not None, "Response should not be None"
        assert "name" in response, "Company name should be present"
        assert "ticker" in response or "symbol" in response, "Ticker or symbol should be present"

    @staticmethod
    def verify_required_profile_fields(response: Dict[str, Any], expected_fields: list = None) -> None:
        if expected_fields is None:
            expected_fields = ["name", "country", "currency", "exchange"]

        for field in expected_fields:
            assert field in response, f"Field '{field}' should be in company profile"

    @staticmethod
    def verify_company_name_exists(response: Dict[str, Any], symbol: str) -> None:
        assert response.get("name"), f"Company name should exist for {symbol}"

    @staticmethod
    def verify_market_cap_valid(response: Dict[str, Any]) -> None:
        if "marketCapitalization" in response:
            market_cap = response["marketCapitalization"]
            assert market_cap > 0, "Market cap should be positive"

    @staticmethod
    def verify_logo_url_valid(response: Dict[str, Any]) -> None:
        if "logo" in response:
            logo = response["logo"]
            assert logo, "Logo URL should not be empty"
            assert "https" in logo.lower(), "Logo should be a valid URL"

    @staticmethod
    def verify_ipo_date_exists(response: Dict[str, Any]) -> None:
        if "ipo" in response:
            ipo_date = response["ipo"]
            assert ipo_date, "IPO date should exist"
            print(f"[OK] IPO Date: {ipo_date}")

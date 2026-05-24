import pytest
from stock_dashboard.api.finnhub_client import FinnhubClient


@pytest.mark.asyncio
@pytest.mark.githubactions
class TestCompanyProfile:
    @pytest.mark.scenario("API: Get company profile with valid symbol")
    async def test_get_company_profile_valid_symbol(self, finnhub_client):
        response = finnhub_client.get_company_profile("AAPL")
        FinnhubClient.verify_company_profile_valid(response)

    @pytest.mark.scenario("API: Company profile has required fields")
    async def test_company_profile_required_fields(self, finnhub_client):
        response = finnhub_client.get_company_profile("AAPL")
        FinnhubClient.verify_required_profile_fields(response)

    @pytest.mark.scenario("API: Get company profile for multiple symbols")
    async def test_company_profile_multiple_symbols(self, finnhub_client):
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        for symbol in symbols:
            response = finnhub_client.get_company_profile(symbol)
            FinnhubClient.verify_company_name_exists(response, symbol)

    @pytest.mark.scenario("API: Company profile contains valid market cap")
    async def test_company_profile_market_cap(self, finnhub_client):
        response = finnhub_client.get_company_profile("AAPL")
        FinnhubClient.verify_market_cap_valid(response)

    @pytest.mark.scenario("API: Company profile contains logo URL")
    async def test_company_profile_logo_url(self, finnhub_client):
        response = finnhub_client.get_company_profile("AAPL")
        FinnhubClient.verify_logo_url_valid(response)

    @pytest.mark.scenario("API: Company profile IPO date")
    async def test_company_profile_ipo_date(self, finnhub_client):
        response = finnhub_client.get_company_profile("AAPL")
        FinnhubClient.verify_ipo_date_exists(response)

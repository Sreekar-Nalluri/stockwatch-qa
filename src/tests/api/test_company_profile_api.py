"""
Company Profile API Tests - Get company information.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get company profile with valid symbol")
async def test_get_company_profile_valid_symbol(finnhub_client):
    response = finnhub_client.get_company_profile("AAPL")
    assert response is not None
    assert "name" in response, "Company name should be present"
    assert "ticker" in response or "symbol" in response

@pytest.mark.asyncio
@pytest.mark.scenario("API: Company profile has required fields")
async def test_company_profile_required_fields(finnhub_client):
    """Verify company profile has required fields."""
    response = finnhub_client.get_company_profile("AAPL")

    expected_fields = ["name", "country", "currency", "exchange"]
    for field in expected_fields:
        assert field in response, f"Field '{field}' should be in company profile"

    print(f"[OK] Profile has fields: {expected_fields}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get company profile for multiple symbols")
async def test_company_profile_multiple_symbols(finnhub_client):
    """Test fetching profiles for multiple companies."""
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

    for symbol in symbols:
        response = finnhub_client.get_company_profile(symbol)
        assert response.get("name"), f"Company name should exist for {symbol}"
        print(f"[OK] {symbol}: {response['name']}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company profile contains valid market cap")
async def test_company_profile_market_cap(finnhub_client):
    """Verify company profile market cap is valid."""
    response = finnhub_client.get_company_profile("AAPL")

    if "marketCapitalization" in response:
        market_cap = response["marketCapitalization"]
        assert market_cap > 0, "Market cap should be positive"
        print(f"[OK] Market Cap: ${market_cap:,.0f}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company profile contains logo URL")
async def test_company_profile_logo_url(finnhub_client):
    """Verify company profile contains logo URL."""
    response = finnhub_client.get_company_profile("AAPL")

    if "logo" in response:
        logo = response["logo"]
        assert logo, "Logo URL should not be empty"
        assert "http" in logo.lower(), "Logo should be a valid URL"
        print(f"[OK] Logo URL: {logo}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company profile contains description")
async def test_company_profile_description(finnhub_client):
    """Verify company profile contains description."""
    response = finnhub_client.get_company_profile("AAPL")

    if "description" in response:
        description = response["description"]
        assert len(description) > 0, "Description should not be empty"
        assert len(description) > 10, "Description should have meaningful content"
        print(f"[OK] Description: {description[:100]}...")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company profile IPO date")
async def test_company_profile_ipo_date(finnhub_client):
    """Verify company profile contains IPO date."""
    response = finnhub_client.get_company_profile("AAPL")

    if "ipo" in response:
        ipo_date = response["ipo"]
        assert ipo_date, "IPO date should exist"
        print(f"[OK] IPO Date: {ipo_date}")


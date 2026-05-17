"""
Quote API Tests - Real-time stock price data.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get stock quote with valid symbol")
async def test_get_quote_valid_symbol(finnhub_client):
    """Test fetching stock quote for valid symbol."""
    response = finnhub_client.get_quote("AAPL")

    assert response is not None
    assert "c" in response, "Current price should be present"
    assert isinstance(response["c"], (int, float))
    assert response["c"] > 0, "Current price should be positive"
    print(f"[OK] AAPL Quote: ${response['c']}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get stock quote with multiple symbols")
async def test_get_quote_multiple_symbols(finnhub_client):
    """Test fetching quotes for multiple symbols."""
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

    for symbol in symbols:
        response = finnhub_client.get_quote(symbol)
        assert response is not None
        assert "c" in response
        assert response["c"] > 0
        print(f"[OK] {symbol}: ${response['c']}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Quote response has required fields")
async def test_quote_response_fields(finnhub_client):
    """Verify quote response has all required fields."""
    response = finnhub_client.get_quote("AAPL")

    required_fields = ["c", "h", "l", "o", "pc", "t"]
    for field in required_fields:
        assert field in response, f"Field '{field}' should be in response"

    print(f"[OK] Quote has all required fields: {required_fields}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Quote data consistency")
async def test_quote_data_consistency(finnhub_client):
    """Verify quote data makes logical sense."""
    response = finnhub_client.get_quote("AAPL")

    current = response["c"]
    high = response["h"]
    low = response["l"]
    prev_close = response["pc"]

    # High should be >= current
    assert high >= current, "High should be >= current price"
    # Low should be <= current
    assert low <= current, "Low should be <= current price"
    # High should be >= low
    assert high >= low, "High should be >= low"

    print(f"[OK] Quote data consistent: C={current}, H={high}, L={low}, PC={prev_close}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Quote timestamp is valid")
async def test_quote_timestamp(finnhub_client):
    """Verify quote timestamp is recent."""
    response = finnhub_client.get_quote("AAPL")

    timestamp = response["t"]
    assert timestamp > 0, "Timestamp should be positive"

    import time
    current_time = int(time.time())
    time_diff = current_time - timestamp

    assert time_diff < 3600, "Quote should be within 1 hour"
    print("[OK] Quote timestamp is recent (${time_diff} seconds old)")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get stock quote error handling")
async def test_get_quote_invalid_symbol(finnhub_client):
    """Test quote API with invalid symbol."""
    try:
        response = finnhub_client.get_quote("INVALID123")
        # API may return empty or error response
        print("[OK] API returned: {response}")
    except Exception as e:
        print(f"[OK] Expected error for invalid symbol: {e}")

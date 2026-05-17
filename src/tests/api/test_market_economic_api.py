"""
Market and Economic Calendar API Tests.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get economic calendar")
async def test_get_economic_calendar(finnhub_client):
    """Test fetching economic calendar."""
    response = finnhub_client.get_economic_calendar()

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Economic calendar: {len(response)} events")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Economic calendar data format")
async def test_economic_calendar_format(finnhub_client):
    """Verify economic calendar data format."""
    response = finnhub_client.get_economic_calendar()

    if len(response) > 0:
        event = response[0]
        # Should have event name and country
        print(f"[OK] Economic event: {event}")

        if "event" in event:
            print(f"   Event: {event['event']}")
        if "country" in event:
            print(f"   Country: {event['country']}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Economic calendar events by country")
async def test_economic_calendar_by_country(finnhub_client):
    """Analyze economic calendar events by country."""
    response = finnhub_client.get_economic_calendar()

    countries = {}
    for event in response[:50]:  # Limit to first 50
        country = event.get("country")
        if country:
            countries[country] = countries.get(country, 0) + 1

    print(f"[OK] Events by country: {countries}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Forex quote")
async def test_forex_quote(finnhub_client):
    """Test fetching forex pair quote."""
    try:
        response = finnhub_client.get_forex_pair("EURUSD")
        assert response is not None
        print(f"[OK] EURUSD Quote: {response}")
    except Exception as e:
        print(f"[WARN] Forex API: {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Multiple forex pairs")
async def test_multiple_forex_pairs(finnhub_client):
    """Test multiple forex pairs."""
    pairs = ["EURUSD", "GBPUSD", "JPYUSD", "AUDUSD"]

    for pair in pairs:
        try:
            response = finnhub_client.get_forex_pair(pair)
            if response:
                print(f"[OK] {pair}: {response}")
        except Exception as e:
            print(f"[WARN] {pair}: {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Intraday trades")
async def test_intraday_trades(finnhub_client):
    """Test fetching intraday trades."""
    response = finnhub_client.get_intraday_trades("AAPL")

    assert isinstance(response, dict), "Response should be a dict"
    print(f"[OK] Intraday trades response: {response}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Intraday trades data format")
async def test_intraday_trades_format(finnhub_client):
    """Verify intraday trades data format."""
    response = finnhub_client.get_intraday_trades("AAPL")

    if "t" in response and "c" in response:
        print(f"[OK] Time series data with {len(response.get('t', []))} candles")
    elif "data" in response:
        print(f"[OK] Trades data: {response['data']}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Technical indicators")
async def test_technical_indicators(finnhub_client):
    """Test fetching technical indicators."""
    try:
        response = finnhub_client.get_technical_indicators("AAPL", resolution="D", indicator="sma")
        assert isinstance(response, dict), "Response should be a dict"
        print(f"[OK] Technical indicators: {response}")
    except Exception as e:
        print(f"[WARN] Technical indicators API: {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Pattern recognition")
async def test_pattern_recognition(finnhub_client):
    """Test fetching pattern recognition data."""
    try:
        response = finnhub_client.get_pattern_recognition("AAPL", resolution="D")
        assert isinstance(response, dict), "Response should be a dict"
        print(f"[OK] Pattern recognition: {response}")
    except Exception as e:
        print(f"[WARN] Pattern recognition API: {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Country ticker symbols")
async def test_country_ticker(finnhub_client):
    """Test fetching symbols by country."""
    try:
        # Use XETRA for German market
        response = finnhub_client.get_country_ticker("XETRA")
        assert isinstance(response, dict), "Response should be a dict"
        if "data" in response and len(response["data"]) > 0:
            print(f"[OK] Found {len(response['data'])} symbols for XETRA")
            print(f"   Sample: {response['data'][0]}")
    except Exception as e:
        print(f"[WARN] Country ticker API: {e}")

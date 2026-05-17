"""
Earnings and Recommendations API Tests.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get earnings surprises")
async def test_get_earnings_surprises(finnhub_client):
    """Test fetching earnings surprises."""
    response = finnhub_client.get_earnings_surprises("AAPL")

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Found {len(response)} earnings surprises for AAPL")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Earnings surprise data validation")
async def test_earnings_surprise_data(finnhub_client):
    """Verify earnings surprise data format."""
    response = finnhub_client.get_earnings_surprises("AAPL")

    if len(response) > 0:
        earning = response[0]
        # Should have period and actual values
        assert "period" in earning or "date" in earning, "Earnings should have period/date"
        print(f"[OK] Earnings data: {earning}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get analyst recommendations")
async def test_get_recommendations(finnhub_client):
    """Test fetching analyst recommendations."""
    response = finnhub_client.get_recommendation_trends("AAPL")

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Found {len(response)} recommendation records for AAPL")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Recommendation trend analysis")
async def test_recommendation_trend_analysis(finnhub_client):
    """Analyze recommendation trends."""
    response = finnhub_client.get_recommendation_trends("AAPL")

    if len(response) > 0:
        latest = response[0]
        print(f"[OK] Latest recommendation: {latest}")

        # Should have buy/hold/sell counts
        if "buy" in latest and "hold" in latest and "sell" in latest:
            buy = latest["buy"]
            hold = latest["hold"]
            sell = latest["sell"]
            total = buy + hold + sell
            if total > 0:
                print(f"[OK] Buy: {buy/total*100:.1f}%, Hold: {hold/total*100:.1f}%, Sell: {sell/total*100:.1f}%")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Recommendations for multiple symbols")
async def test_recommendations_multiple_symbols(finnhub_client):
    """Test recommendations for multiple companies."""
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]

    for symbol in symbols:
        response = finnhub_client.get_recommendation_trends(symbol)
        if len(response) > 0:
            print(f"[OK] {symbol}: {len(response)} recommendation records")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Earnings calendar for specific symbol")
async def test_earnings_calendar_symbol(finnhub_client):
    """Test earnings calendar with symbol filter."""
    response = finnhub_client.get_earnings_calendar("AAPL")

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] AAPL earnings calendar: {len(response)} events")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Earnings calendar general")
async def test_earnings_calendar_general(finnhub_client):
    """Test general earnings calendar."""
    response = finnhub_client.get_earnings_calendar()

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] General earnings calendar: {len(response)} events")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Earnings calendar data validation")
async def test_earnings_calendar_data(finnhub_client):
    """Verify earnings calendar data format."""
    response = finnhub_client.get_earnings_calendar()

    if len(response) > 0:
        event = response[0]
        # Should have symbol and date
        assert "symbol" in event or "ticker" in event, "Event should have symbol"
        print(f"[OK] Calendar event: {event}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: IPO calendar")
async def test_ipo_calendar(finnhub_client):
    """Test fetching IPO calendar."""
    response = finnhub_client.get_ipo_calendar()

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] IPO calendar: {len(response)} upcoming IPOs")


@pytest.mark.asyncio
@pytest.mark.scenario("API: IPO calendar data validation")
async def test_ipo_calendar_data(finnhub_client):
    """Verify IPO calendar data format."""
    response = finnhub_client.get_ipo_calendar()

    if len(response) > 0:
        ipo = response[0]
        print(f"[OK] IPO: {ipo}")

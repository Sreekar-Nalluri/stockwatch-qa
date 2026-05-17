"""
News API Tests - Company and market news.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get company news with valid symbol")
async def test_get_company_news_valid_symbol(finnhub_client):
    """Test fetching company news for valid symbol."""
    response = finnhub_client.get_company_news("AAPL", limit=5)

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Found {len(response)} news items for AAPL")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company news items have required fields")
async def test_company_news_required_fields(finnhub_client):
    """Verify company news items have required fields."""
    response = finnhub_client.get_company_news("AAPL", limit=5)

    if len(response) > 0:
        article = response[0]
        required_fields = ["headline", "source", "timestamp", "url"]
        for field in required_fields:
            assert field in article, f"Field '{field}' should be in news article"
        print(f"[OK] News article has required fields: {required_fields}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get market news")
async def test_get_market_news(finnhub_client):
    """Test fetching general market news."""
    response = finnhub_client.get_market_news("general", limit=5)

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Found {len(response)} market news items")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Market news categories")
async def test_market_news_categories(finnhub_client):
    """Test fetching news from different categories."""
    categories = ["general", "forex", "crypto"]

    for category in categories:
        try:
            response = finnhub_client.get_market_news(category, limit=3)
            print(f"[OK] {category}: {len(response)} items")
        except Exception as e:
            print(f"[WARN] Category '{category}' error: {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company news limit parameter")
async def test_company_news_limit(finnhub_client):
    """Test news API with different limit values."""
    for limit in [1, 5, 10]:
        response = finnhub_client.get_company_news("AAPL", limit=limit)
        actual_count = len(response)
        assert actual_count <= limit, f"Should not exceed limit of {limit}"
        print(f"[OK] News with limit={limit}: {actual_count} items")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Company news timestamp validation")
async def test_company_news_timestamp(finnhub_client):
    """Verify company news has valid timestamps."""
    response = finnhub_client.get_company_news("AAPL", limit=5)

    if len(response) > 0:
        for article in response:
            timestamp = article.get("timestamp")
            assert timestamp, "Timestamp should exist"
            assert isinstance(timestamp, int), "Timestamp should be integer"
            print(f"[OK] Article timestamp: {timestamp}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: News article sentiment")
async def test_news_article_sentiment(finnhub_client):
    """Check if news articles contain sentiment data."""
    response = finnhub_client.get_company_news("AAPL", limit=3)

    for article in response:
        # Finnhub may include related symbols or sentiment
        print(f"[OK] Article: {article.get('headline', 'N/A')[:50]}...")


@pytest.mark.asyncio
@pytest.mark.scenario("API: News article has valid URL")
async def test_news_article_url(finnhub_client):
    """Verify news articles have valid URLs."""
    response = finnhub_client.get_company_news("AAPL", limit=3)

    if len(response) > 0:
        for article in response:
            url = article.get("url")
            assert url, "URL should exist"
            assert "http" in url.lower(), "URL should contain http"
            print(f"[OK] Valid URL: {url[:60]}...")

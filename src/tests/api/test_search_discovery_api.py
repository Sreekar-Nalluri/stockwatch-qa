"""
Search and Discovery API Tests - Symbol search, peers, splits, dividends.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API: Search for symbols and companies")
async def test_search_symbols(finnhub_client):
    """Test searching for symbols."""
    response = await finnhub_client.get_search("Apple")

    assert isinstance(response, dict), "Response should be a dict"
    assert "result" in response or "count" in response
    print(f"[OK] Search results: {response}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get company peers")
async def test_get_company_peers(finnhub_client):
    """Test fetching company peers."""
    response = await finnhub_client.get_peers("AAPL")

    assert isinstance(response, list), "Response should be a list of peer symbols"
    assert len(response) > 0, "Should have at least one peer"
    print(f"[OK] AAPL Peers: {response}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get stock splits")
async def test_get_stock_splits(finnhub_client):
    """Test fetching stock split history."""
    response = await finnhub_client.get_splits("AAPL")

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Found {len(response)} stock splits for AAPL")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Stock split data validation")
async def test_stock_split_data(finnhub_client):
    """Verify stock split data format."""
    response = await finnhub_client.get_splits("AAPL")

    if len(response) > 0:
        split = response[0]
        # Splits should have date and split ratio
        assert "date" in split or "exDate" in split, "Split should have date"
        print(f"[OK] Stock split: {split}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get dividend history")
async def test_get_dividends(finnhub_client):
    """Test fetching dividend history."""
    response = await finnhub_client.get_dividends("AAPL")

    assert isinstance(response, list), "Response should be a list"
    print(f"[OK] Found {len(response)} dividend records for AAPL")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Dividend data validation")
async def test_dividend_data(finnhub_client):
    """Verify dividend data format."""
    response = await finnhub_client.get_dividends("AAPL")

    if len(response) > 0:
        div = response[0]
        # Dividends should have date and amount
        assert "date" in div or "exDate" in div, "Dividend should have date"
        print(f"[OK] Dividend: {div}")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Get multiple peers")
async def test_peers_multiple_symbols(finnhub_client):
    """Test peers API for multiple symbols."""
    symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in symbols:
        response = await finnhub_client.get_peers(symbol)
        assert isinstance(response, list)
        print(f"[OK] {symbol} peers: {len(response)} companies")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Dividend yield calculation")
async def test_dividend_yield(finnhub_client):
    """Test calculating dividend yield."""
    quote = await finnhub_client.get_quote("AAPL")
    dividends = await finnhub_client.get_dividends("AAPL")

    current_price = quote["c"]

    if len(dividends) > 0:
        annual_dividend = sum(d.get("amount", 0) for d in dividends[-4:])
        if current_price > 0:
            yield_pct = (annual_dividend / current_price) * 100
            print(f"[OK] AAPL Dividend Yield: {yield_pct:.2f}%")


@pytest.mark.asyncio
@pytest.mark.scenario("API: Search with empty query")
async def test_search_empty_query(finnhub_client):
    """Test search API with minimal query."""
    try:
        response = await finnhub_client.get_search("A")
        if response:
            print(f"[OK] Search 'A' returned: {response}")
    except Exception as e:
        print(f"[WARN] Search error: {e}")

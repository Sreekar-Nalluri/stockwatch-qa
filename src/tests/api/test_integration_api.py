"""
Integration API Tests - Multi-API scenarios.
"""

import pytest


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Get complete stock profile")
async def test_complete_stock_profile(finnhub_client):
    """
    Integration test: Get complete stock profile combining multiple APIs.

    Fetches quote, company profile, and news for a symbol.
    """
    symbol = "AAPL"

    print(f"\n[INFO] Fetching complete profile for {symbol}...")

    # Get quote
    quote = finnhub_client.get_quote(symbol)
    assert quote["c"] > 0

    # Get company profile
    profile = finnhub_client.get_company_profile(symbol)
    assert "name" in profile

    # Get news
    news = finnhub_client.get_company_news(symbol, limit=5)

    print(f"[OK] {symbol} Complete Profile:")
    print(f"   Price: ${quote['c']}")
    print(f"   Company: {profile.get('name', 'N/A')}")
    print(f"   Recent News: {len(news)} articles")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Analyze stock fundamentals")
async def test_stock_fundamentals_analysis(finnhub_client):
    """
    Integration test: Analyze stock fundamentals.

    Combines quote, profile, splits, dividends, and recommendations.
    """
    symbol = "MSFT"

    print(f"\n[INFO] Analyzing fundamentals for {symbol}...")

    quote = finnhub_client.get_quote(symbol)
    profile = finnhub_client.get_company_profile(symbol)
    dividends = finnhub_client.get_dividends(symbol)
    recommendations = finnhub_client.get_recommendation_trends(symbol)

    current_price = quote["c"]

    # Calculate metrics
    print(f"[OK] {symbol} Fundamentals Analysis:")
    print(f"   Current Price: ${current_price}")
    print(f"   Market Cap: ${profile.get('marketCapitalization', 'N/A')}")
    print(f"   Dividend Records: {len(dividends)}")

    if len(recommendations) > 0:
        latest_rec = recommendations[0]
        if "buy" in latest_rec:
            total = latest_rec["buy"] + latest_rec["hold"] + latest_rec["sell"]
            buy_pct = (latest_rec["buy"] / total * 100) if total > 0 else 0
            print(f"   Analyst Buy: {buy_pct:.1f}%")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Compare peer companies")
async def test_compare_peers(finnhub_client):
    """
    Integration test: Compare peer companies.

    Gets peers and fetches quotes for all.
    """
    symbol = "AAPL"

    print(f"\n[INFO] Comparing {symbol} with peers...")

    # Get peers
    peers = finnhub_client.get_peers(symbol)
    print(f"[OK] Peers for {symbol}: {peers[:5]}")

    # Get quotes for symbol and first 3 peers
    quote = finnhub_client.get_quote(symbol)
    comparison = {symbol: quote["c"]}

    for peer in peers[:3]:
        try:
            peer_quote = finnhub_client.get_quote(peer)
            comparison[peer] = peer_quote["c"]
        except:
            pass

    print(f"[OK] Price Comparison:")
    for comp_symbol, price in comparison.items():
        print(f"   {comp_symbol}: ${price}")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Track earnings season")
async def test_earnings_season_tracking(finnhub_client):
    """
    Integration test: Track earnings season.

    Gets earnings calendar and earnings surprises for symbols.
    """
    print("\n[INFO] Tracking earnings season...")

    # Get earnings calendar
    calendar = finnhub_client.get_earnings_calendar()

    # Get earnings surprises for specific stocks
    symbols = ["AAPL", "MSFT", "GOOGL"]

    print(f"[OK] Calendar events: {len(calendar)}")

    for symbol in symbols:
        try:
            surprises = finnhub_client.get_earnings_surprises(symbol)
            print(f"   {symbol}: {len(surprises)} earnings records")
        except Exception as e:
            print(f"   {symbol}: {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Market sectors overview")
async def test_market_sectors_overview(finnhub_client):
    """
    Integration test: Get market overview across sectors.

    Fetches quotes for multiple sectors.
    """
    print("\n[INFO] Market sectors overview...")

    # Representative symbols from different sectors
    sectors = {
        "Technology": ["AAPL", "MSFT", "GOOGL"],
        "Finance": ["JPM", "BAC", "GS"],
        "Energy": ["XOM", "CVX"],
        "Healthcare": ["JNJ", "UNH"]
    }

    for sector, symbols in sectors.items():
        print(f"\n[OK] {sector}:")
        for symbol in symbols:
            try:
                quote = finnhub_client.get_quote(symbol)
                print(f"   {symbol}: ${quote['c']}")
            except Exception as e:
                print(f"   {symbol}: Error - {e}")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Portfolio performance check")
async def test_portfolio_performance(finnhub_client):
    """
    Integration test: Check portfolio performance.

    Gets quotes for a hypothetical portfolio.
    """
    portfolio = {
        "AAPL": 10,    # 10 shares
        "MSFT": 5,     # 5 shares
        "GOOGL": 3     # 3 shares
    }

    print("\n[INFO] Portfolio Performance Check...")

    total_value = 0
    for symbol, shares in portfolio.items():
        quote = finnhub_client.get_quote(symbol)
        price = quote["c"]
        value = price * shares
        total_value += value
        print(f"[OK] {symbol}: {shares} shares @ ${price} = ${value:.2f}")

    print(f"\n[OK] Total Portfolio Value: ${total_value:.2f}")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Technical analysis preparation")
async def test_technical_analysis_data(finnhub_client):
    """
    Integration test: Prepare data for technical analysis.

    Gets historical data and technical indicators.
    """
    symbol = "AAPL"

    print(f"\n[INFO] Preparing technical analysis for {symbol}...")

    # Get current quote
    quote = finnhub_client.get_quote(symbol)
    print(f"[OK] Current price: ${quote['c']}")

    # Try to get intraday trades
    try:
        trades = finnhub_client.get_intraday_trades(symbol)
        print(f"[OK] Intraday data available")
    except:
        print(f"[WARN] Intraday data not available")

    # Try to get technical indicators
    try:
        indicators = finnhub_client.get_technical_indicators(symbol, indicator="sma")
        print(f"[OK] Technical indicators available")
    except:
        print(f"[WARN] Technical indicators not available")


@pytest.mark.asyncio
@pytest.mark.scenario("API Integration: Real-time market alerts")
async def test_market_alert_system(finnhub_client):
    """
    Integration test: Check market conditions for alerts.

    Gets multiple data points to trigger hypothetical alerts.
    """
    print("\n[INFO] Real-time Market Alert Check...")

    symbols = ["AAPL", "MSFT", "TSLA"]

    for symbol in symbols:
        quote = finnhub_client.get_quote(symbol)

        current = quote["c"]
        high = quote["h"]
        low = quote["l"]

        # Calculate range
        range_pct = ((high - low) / low * 100) if low > 0 else 0

        # Hypothetical alert thresholds
        if range_pct > 5:
            print(f"[ALERT] {symbol}: High volatility (range: {range_pct:.2f}%)")

        # Price near high
        if current >= high * 0.98:
            print(f"[ALERT] {symbol}: Price near daily high (${current})")


"""
Async Playwright Test: Dashboard with API Key and Data Loading

Scenario:
1. Launch dashboard
2. Enter API key and load data
3. Verify data is getting loaded

Uses async/await pattern with DashboardPage helper methods.
All locators are centralized in DashboardPage class.
"""

import pytest
from playwright.async_api import Page


@pytest.mark.asyncio
@pytest.mark.scenario("Dashboard: Launch, enter API key, and load stock data (ASYNC)")
async def test_dashboard_load_stock_data_async(test_context):
    """
    Test: Dashboard load stock data workflow (ASYNC)

    Uses helper methods from DashboardPage to manage all interactions.

    Steps:
    1. Navigate to dashboard (already done by fixture)
    2. Enter Finnhub API key
    3. Click LOAD DATA button
    4. Wait for data to load and verify
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    # Initialize page object with all locators and helpers
    dashboard = DashboardPage(page)

    print("=" * 60)
    print("TEST: Dashboard Data Load (ASYNC)")
    print("=" * 60)

    # ===== STEP 1: Verify initial state =====
    print("\n[STEP 1] Verifying initial state...")
    is_error_visible = await dashboard.is_error_visible()
    assert not is_error_visible, "Error message should be hidden initially"
    print("✓ Error message is hidden")

    last_updated = await dashboard.get_last_updated()
    assert last_updated == "—", f"Last updated should be '—' initially, got: {last_updated}"
    print("✓ Last updated is '—'")

    # ===== STEP 2: Enter API key =====
    print("\n[STEP 2] Entering API key...")
    await dashboard.enter_api_key(api_key)

    # Verify key is entered
    key_value = await dashboard.api_key_input.input_value()
    assert key_value == api_key, f"API key not entered correctly. Got: {key_value}"
    print(f"✓ API key entered: {api_key[:10]}...")

    # ===== STEP 3: Click LOAD DATA button =====
    print("\n[STEP 3] Clicking LOAD DATA button...")
    await dashboard.click_load_button()
    print("✓ LOAD DATA button clicked")

    # ===== STEP 4: Wait for data to load =====
    print("\n[STEP 4] Waiting for data to load...")
    await dashboard.wait_for_data_load(timeout=5000)
    print("✓ Data load timeout completed")

    # ===== STEP 5: Verify market status =====
    print("\n[STEP 5] Verifying market status...")
    market_status = await dashboard.get_market_status()
    assert market_status in ["MARKET OPEN", "MARKET CLOSED"], \
        f"Market status should be OPEN or CLOSED, got: {market_status}"
    print(f"✓ Market status: {market_status}")

    # Verify status dot
    status_class = await dashboard.get_status_dot_class()
    assert "open" in status_class or "closed" in status_class, \
        f"Status dot should have 'open' or 'closed' class, got: {status_class}"
    print(f"✓ Status dot class: {status_class}")

    # ===== STEP 6: Verify last updated timestamp =====
    print("\n[STEP 6] Verifying last updated timestamp...")
    last_updated = await dashboard.get_last_updated()
    assert last_updated != "—", "Last updated timestamp should be set after loading data"
    print(f"✓ Last updated: {last_updated}")

    # ===== STEP 7: Verify stock cards =====
    print("\n[STEP 7] Verifying stock cards...")
    cards_count = await dashboard.get_stock_cards_count()
    assert cards_count >= 3, f"Should have at least 3 stock cards, got: {cards_count}"
    print(f"✓ Stock cards loaded: {cards_count}")

    # ===== STEP 8: Verify first card (AAPL) =====
    print("\n[STEP 8] Verifying AAPL card (first stock card)...")

    aapl_symbol = await dashboard.get_first_card_symbol()
    assert "AAPL" in aapl_symbol, f"AAPL symbol should be in first card, got: {aapl_symbol}"
    print(f"✓ AAPL symbol: {aapl_symbol}")

    aapl_price = await dashboard.get_first_card_price()
    assert "$" in aapl_price, f"AAPL price should contain $, got: {aapl_price}"
    print(f"✓ AAPL price: {aapl_price}")

    aapl_change = await dashboard.get_first_card_change()
    assert aapl_change, "AAPL change should be displayed"
    print(f"✓ AAPL change: {aapl_change}")

    aapl_open = await dashboard.get_first_card_open_price()
    assert "$" in aapl_open, f"AAPL open price should contain $, got: {aapl_open}"
    print(f"✓ AAPL open price: {aapl_open}")

    aapl_high = await dashboard.get_first_card_high_price()
    assert "$" in aapl_high, f"AAPL day high should contain $, got: {aapl_high}"
    print(f"✓ AAPL day high: {aapl_high}")

    aapl_low = await dashboard.get_first_card_low_price()
    assert "$" in aapl_low, f"AAPL day low should contain $, got: {aapl_low}"
    print(f"✓ AAPL day low: {aapl_low}")

    aapl_prev_close = await dashboard.get_first_card_prev_close()
    assert "$" in aapl_prev_close, f"AAPL prev close should contain $, got: {aapl_prev_close}"
    print(f"✓ AAPL prev close: {aapl_prev_close}")

    # ===== STEP 9: Verify second card (MSFT) =====
    print("\n[STEP 9] Verifying MSFT card (second stock card)...")

    msft_symbol = await dashboard.get_nth_card_symbol(2)
    assert "MSFT" in msft_symbol, f"MSFT symbol should be in second card, got: {msft_symbol}"
    print(f"✓ MSFT symbol: {msft_symbol}")

    msft_price = await dashboard.get_nth_card_price(2)
    assert "$" in msft_price, f"MSFT price should contain $, got: {msft_price}"
    print(f"✓ MSFT price: {msft_price}")

    # ===== STEP 10: Verify third card (GOOGL) =====
    print("\n[STEP 10] Verifying GOOGL card (third stock card)...")

    googl_symbol = await dashboard.get_nth_card_symbol(3)
    assert "GOOGL" in googl_symbol, f"GOOGL symbol should be in third card, got: {googl_symbol}"
    print(f"✓ GOOGL symbol: {googl_symbol}")

    googl_price = await dashboard.get_nth_card_price(3)
    assert "$" in googl_price, f"GOOGL price should contain $, got: {googl_price}"
    print(f"✓ GOOGL price: {googl_price}")

    # ===== STEP 11: Verify detail table =====
    print("\n[STEP 11] Verifying detail table...")

    detail_visible = await dashboard.is_detail_section_visible()
    assert detail_visible, "Detail section should be visible after data load"
    print("✓ Detail section is visible")

    table_rows = await dashboard.get_detail_table_rows_count()
    assert table_rows >= 3, f"Detail table should have at least 3 rows, got: {table_rows}"
    print(f"✓ Detail table rows: {table_rows}")

    # ===== STEP 12: Verify detail table data =====
    print("\n[STEP 12] Verifying detail table data...")

    aapl_table_current = await dashboard.get_aapl_table_current_price()
    assert "$" in aapl_table_current, f"AAPL table current price should contain $, got: {aapl_table_current}"
    print(f"✓ AAPL table current price: {aapl_table_current}")

    aapl_table_change = await dashboard.get_aapl_table_change()
    assert "%" in aapl_table_change, f"AAPL table change should contain %, got: {aapl_table_change}"
    print(f"✓ AAPL table change: {aapl_table_change}")

    msft_table_current = await dashboard.get_msft_table_current_price()
    assert "$" in msft_table_current, f"MSFT table current price should contain $, got: {msft_table_current}"
    print(f"✓ MSFT table current price: {msft_table_current}")

    msft_table_change = await dashboard.get_msft_table_change()
    assert "%" in msft_table_change, f"MSFT table change should contain %, got: {msft_table_change}"
    print(f"✓ MSFT table change: {msft_table_change}")

    googl_table_current = await dashboard.get_googl_table_current_price()
    assert "$" in googl_table_current, f"GOOGL table current price should contain $, got: {googl_table_current}"
    print(f"✓ GOOGL table current price: {googl_table_current}")

    googl_table_change = await dashboard.get_googl_table_change()
    assert "%" in googl_table_change, f"GOOGL table change should contain %, got: {googl_table_change}"
    print(f"✓ GOOGL table change: {googl_table_change}")

    # ===== TEST PASSED =====
    print("\n" + "=" * 60)
    print("✅ TEST PASSED: Dashboard data loaded successfully (ASYNC)")
    print("=" * 60)
    print(f"Market Status: {market_status}")
    print(f"Last Updated: {last_updated}")
    print(f"Stock Cards: {cards_count}")
    print(f"Table Rows: {table_rows}")
    print("=" * 60)


@pytest.mark.asyncio
@pytest.mark.scenario("Dashboard: Verify price change indicators (up/down/flat) (ASYNC)")
async def test_dashboard_price_indicators_async(test_context):
    """
    Test: Verify stock cards show correct price change indicators

    Verifies visual indicators for price movement:
    - Up arrow (▲) when price > previous close
    - Down arrow (▼) when price < previous close
    - Dash (—) when price = previous close
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    dashboard = DashboardPage(page)

    print("\n[TEST] Dashboard Price Indicators (ASYNC)")

    # Navigate and load data
    await dashboard.load_data_with_key(api_key)
    await dashboard.wait_for_data_load(timeout=5000)

    # Check AAPL price change
    aapl_change = await dashboard.get_first_card_change()
    assert "▲" in aapl_change or "▼" in aapl_change or "—" in aapl_change, \
        f"AAPL change should have indicator (▲/▼/—), got: {aapl_change}"
    print(f"✓ AAPL price change indicator: {aapl_change}")

    # Check MSFT price change
    msft_change = await dashboard.get_nth_card_change(2)
    assert "▲" in msft_change or "▼" in msft_change or "—" in msft_change, \
        f"MSFT change should have indicator, got: {msft_change}"
    print(f"✓ MSFT price change indicator: {msft_change}")

    # Check GOOGL price change
    googl_change = await dashboard.get_nth_card_change(3)
    assert "▲" in googl_change or "▼" in googl_change or "—" in googl_change, \
        f"GOOGL change should have indicator, got: {googl_change}"
    print(f"✓ GOOGL price change indicator: {googl_change}")

    print("✅ TEST PASSED: Price indicators verified")


@pytest.mark.asyncio
@pytest.mark.scenario("Dashboard: No auto-load without button click (ASYNC)")
async def test_dashboard_no_auto_load_async(test_context):
    """
    Test: Entering API key without clicking LOAD DATA should not load data

    Verifies:
    - Data is not loaded automatically on key entry
    - User must click LOAD DATA button to fetch data
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    dashboard = DashboardPage(page)

    print("\n[TEST] No Auto-Load Without Button Click (ASYNC)")

    # Enter API key but don't click button
    await dashboard.enter_api_key(api_key)
    print("✓ Entered API key (without clicking LOAD DATA)")

    # Wait a moment
    await dashboard.wait_for_data_load(timeout=1000)

    # Verify no cards are loaded yet
    last_updated = await dashboard.get_last_updated()
    assert last_updated == "—", \
        f"Last updated should still be '—' without clicking LOAD DATA, got: {last_updated}"
    print(f"✓ Last updated still '—': {last_updated}")

    print("✅ TEST PASSED: Data not auto-loaded without button click")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


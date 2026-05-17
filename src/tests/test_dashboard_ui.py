"""
UI Test: Dashboard - Launch, Enter API Key, Load Data, Verify
Uses Playwright async API to interact with dashboard UI.
Server starts automatically via conftest fixture and closes after tests complete.
"""

import pytest
from playwright.async_api import Page


@pytest.mark.asyncio
@pytest.mark.scenario("UI: Dashboard - Enter API key, load data, verify data loaded")
async def test_dashboard_ui_load_data(test_context):
    """
    Complete UI test flow: Launch -> Enter Key -> Load -> Verify

    Steps:
    1. Page navigates to dashboard (done by test_context fixture)
    2. Enter valid API key into input field
    3. Click LOAD DATA button
    4. Wait for data to load
    5. Verify all data is displayed correctly on UI
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    dashboard = DashboardPage(page)

    print("\n" + "="*70)
    print("UI TEST: Dashboard Load Data Workflow")
    print("="*70)

    # Step 1: Verify initial state
    print("\n[Step 1] Verify initial dashboard state...")
    initial_status = await dashboard.get_last_updated()
    assert initial_status == "—", f"Should start with no data, got: {initial_status}"
    print("[OK] Dashboard is empty initially")

    # Step 2: Enter API key
    print("\n[Step 2] Enter API key into input field...")
    await dashboard.enter_api_key(api_key)
    entered_key = await dashboard.api_key_input.input_value()
    assert entered_key == api_key, "API key not entered correctly"
    print("[OK] API key entered successfully")

    # Step 3: Click LOAD DATA button
    print("\n[Step 3] Click LOAD DATA button...")
    await dashboard.click_load_button()
    print("[OK] LOAD DATA button clicked")

    # Step 4: Wait for data to load
    print("\n[Step 4] Wait for data to load (5 seconds)...")
    await dashboard.wait_for_data_load(timeout=5000)
    print("[OK] Data load timeout completed")

    # Step 5: Verify data is loaded
    print("\n[Step 5] Verify data is loaded on UI...")

    # Check market status
    market_status = await dashboard.get_market_status()
    assert market_status in ["MARKET OPEN", "MARKET CLOSED"], \
        f"Invalid market status: {market_status}"
    print(f"[OK] Market status displayed: {market_status}")

    # Check last updated timestamp
    last_updated = await dashboard.get_last_updated()
    assert last_updated != "—", "Last updated should be set after loading data"
    print(f"[OK] Last updated timestamp: {last_updated}")

    # Check stock cards are loaded
    cards_count = await dashboard.get_stock_cards_count()
    assert cards_count >= 3, f"Expected at least 3 cards, got: {cards_count}"
    print(f"[OK] Stock cards loaded: {cards_count}")

    # Step 6: Verify first card data (AAPL)
    print("\n[Step 6] Verify first stock card (AAPL) data...")

    aapl_symbol = await dashboard.get_first_card_symbol()
    assert "AAPL" in aapl_symbol, f"AAPL symbol not found: {aapl_symbol}"
    print(f"[OK] Symbol: {aapl_symbol}")

    aapl_price = await dashboard.get_first_card_price()
    assert "$" in aapl_price, f"Price should contain $: {aapl_price}"
    print(f"[OK] Current price: {aapl_price}")

    aapl_change = await dashboard.get_first_card_change()
    assert aapl_change, "Price change should be displayed"
    print(f"[OK] Price change: {aapl_change}")

    aapl_open = await dashboard.get_first_card_open_price()
    assert "$" in aapl_open, f"Open price should contain $: {aapl_open}"
    print(f"[OK] Open price: {aapl_open}")

    aapl_high = await dashboard.get_first_card_high_price()
    assert "$" in aapl_high, f"Day high should contain $: {aapl_high}"
    print(f"[OK] Day high: {aapl_high}")

    aapl_low = await dashboard.get_first_card_low_price()
    assert "$" in aapl_low, f"Day low should contain $: {aapl_low}"
    print(f"[OK] Day low: {aapl_low}")

    # Step 7: Verify detail section is visible
    print("\n[Step 7] Verify detail section is visible...")
    detail_visible = await dashboard.is_detail_section_visible()
    assert detail_visible, "Detail section should be visible"
    print("[OK] Detail section visible")

    table_rows = await dashboard.get_detail_table_rows_count()
    assert table_rows >= 3, f"Detail table should have at least 3 rows, got: {table_rows}"
    print(f"[OK] Detail table rows: {table_rows}")

    # Step 8: Verify detail table data
    print("\n[Step 8] Verify detail table data...")
    aapl_table_price = await dashboard.get_aapl_table_current_price()
    assert "$" in aapl_table_price, f"Table AAPL price should contain $: {aapl_table_price}"
    print(f"[OK] AAPL table price: {aapl_table_price}")

    aapl_table_change = await dashboard.get_aapl_table_change()
    assert "%" in aapl_table_change, f"Table AAPL change should contain %: {aapl_table_change}"
    print(f"[OK] AAPL table change: {aapl_table_change}")

    # Test completed successfully
    print("\n" + "="*70)
    print("[PASS] UI TEST PASSED: Dashboard data loaded and verified")
    print("="*70)
    print(f"Market Status: {market_status}")
    print(f"Last Updated: {last_updated}")
    print(f"Stock Cards: {cards_count}")
    print(f"Detail Rows: {table_rows}")
    print("="*70)


@pytest.mark.asyncio
@pytest.mark.scenario("UI: Dashboard - Verify data verification method")
async def test_dashboard_verify_data_loaded(test_context):
    """
    Test the verify_data_loaded() helper method
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    dashboard = DashboardPage(page)

    print("\n[TEST] Dashboard verify_data_loaded() method")

    # Initially, data should not be loaded
    is_loaded = await dashboard.verify_data_loaded()
    assert not is_loaded, "Data should not be loaded initially"
    print("[OK] Initially data not loaded")

    # Load data
    await dashboard.load_data_with_key(api_key)
    await dashboard.wait_for_data_load(timeout=5000)

    # Now data should be loaded
    is_loaded = await dashboard.verify_data_loaded()
    assert is_loaded, "Data should be loaded after clicking button"
    print("[OK] Data verified as loaded")

    print("[PASS] TEST PASSED: verify_data_loaded() method works correctly")


@pytest.mark.asyncio
@pytest.mark.scenario("UI: Dashboard - No auto-load without button click")
async def test_dashboard_no_auto_load(test_context):
    """
    Verify data is not loaded automatically without clicking LOAD DATA button
    """
    from src.pages.dashboard_page import DashboardPage

    page = test_context['page']
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"

    dashboard = DashboardPage(page)

    print("\n[TEST] Dashboard no auto-load test")

    # Enter API key but don't click button
    await dashboard.enter_api_key(api_key)
    print("[OK] API key entered (button NOT clicked)")

    # Wait a moment
    await dashboard.wait_for_data_load(timeout=1000)

    # Verify data is still NOT loaded
    last_updated = await dashboard.get_last_updated()
    assert last_updated == "—", f"Data should not load without button click, got: {last_updated}"
    print("[OK] Data NOT auto-loaded without button click")

    cards_count = await dashboard.get_stock_cards_count()
    assert cards_count == 0, f"No cards should be loaded, got: {cards_count}"
    print("[OK] No stock cards loaded")

    print("[PASS] TEST PASSED: Data not auto-loaded without button click")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


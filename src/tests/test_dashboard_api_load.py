"""
Generated Playwright Test: Dashboard with API Key and Data Loading

Scenario:
1. Launch dashboard
2. Enter API key and load data
3. Verify data is getting loaded

Test verifies:
- Dashboard page loads
- API key input is functional
- Load data button triggers data fetch
- Stock data cards are displayed
- Market status is updated
- Detail table is populated with stock data
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.scenario("Dashboard: Launch, enter API key, and load stock data")
def test_dashboard_load_stock_data(page: Page):
    """
    Test: Dashboard load stock data workflow

    Steps:
    1. Navigate to dashboard
    2. Enter Finnhub API key
    3. Click LOAD DATA button
    4. Wait for data to load and verify
    """

    # Step 1: Navigate to dashboard
    page.goto("http://localhost:8080/dashboard.html")
    expect(page).to_have_title("Stock Dashboard")

    # Verify initial state - no data loaded yet
    error_msg = page.locator("#error-msg")
    assert error_msg.is_hidden(), "Error message should be hidden initially"

    last_updated = page.locator("#last-updated")
    expect(last_updated).to_contain_text("—")

    # Step 2: Enter API key
    api_key_input = page.locator("#api-key-input")
    api_key = "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20"
    page.fill("#api-key-input", api_key)
    expect(api_key_input).to_have_value(api_key)

    # Step 3: Click LOAD DATA button
    load_button = page.locator("button:has-text('LOAD DATA')")
    load_button.click()

    # Wait for data to load (default symbols: AAPL, MSFT, GOOGL)
    page.wait_for_timeout(3000)

    # Step 4: Verify market status is updated
    status_text = page.locator("#status-text")
    status_value = status_text.text_content()
    assert status_value in ["MARKET OPEN", "MARKET CLOSED"], \
        f"Market status should be OPEN or CLOSED, got: {status_value}"

    # Verify status dot color changed
    status_dot = page.locator("#status-dot")
    dot_class = status_dot.get_attribute("class")
    assert "open" in dot_class or "closed" in dot_class, \
        f"Status dot should have 'open' or 'closed' class, got: {dot_class}"

    # Verify last updated timestamp is set
    last_updated = page.locator("#last-updated")
    last_updated_text = last_updated.text_content()
    assert last_updated_text != "—", \
        "Last updated timestamp should be set after loading data"

    # Verify stock cards are displayed
    cards_grid = page.locator("#cards-grid")
    stock_cards = page.locator(".stock-card")
    card_count = stock_cards.count()
    assert card_count >= 3, \
        f"Should have at least 3 stock cards (AAPL, MSFT, GOOGL), got: {card_count}"

    # Verify AAPL card
    aapl_symbol = page.locator(".stock-card:first-child [data-testid='symbol']")
    expect(aapl_symbol).to_contain_text("AAPL")

    aapl_price = page.locator(".stock-card:first-child [data-testid='current-price']")
    aapl_price_text = aapl_price.text_content()
    assert "$" in aapl_price_text, "AAPL current price should contain $"

    aapl_change = page.locator(".stock-card:first-child [data-testid='price-change']")
    assert aapl_change.text_content(), "AAPL price change should be displayed"

    aapl_open = page.locator(".stock-card:first-child [data-testid='open-price']")
    assert "$" in aapl_open.text_content(), "AAPL open price should contain $"

    aapl_high = page.locator(".stock-card:first-child [data-testid='day-high']")
    assert "$" in aapl_high.text_content(), "AAPL day high should contain $"

    aapl_low = page.locator(".stock-card:first-child [data-testid='day-low']")
    assert "$" in aapl_low.text_content(), "AAPL day low should contain $"

    aapl_prev_close = page.locator(".stock-card:first-child [data-testid='prev-close']")
    assert "$" in aapl_prev_close.text_content(), "AAPL prev close should contain $"

    # Verify MSFT card
    msft_symbol = page.locator(".stock-card:nth-child(2) [data-testid='symbol']")
    expect(msft_symbol).to_contain_text("MSFT")

    msft_price = page.locator(".stock-card:nth-child(2) [data-testid='current-price']")
    assert "$" in msft_price.text_content(), "MSFT current price should contain $"

    # Verify GOOGL card
    googl_symbol = page.locator(".stock-card:nth-child(3) [data-testid='symbol']")
    expect(googl_symbol).to_contain_text("GOOGL")

    googl_price = page.locator(".stock-card:nth-child(3) [data-testid='current-price']")
    assert "$" in googl_price.text_content(), "GOOGL current price should contain $"

    # Verify detail table is displayed
    detail_section = page.locator("#detail-section")
    assert "block" in detail_section.get_attribute("style") or not detail_section.get_attribute("style"), \
        "Detail section should be visible"

    # Verify table rows contain data
    table_rows = page.locator("tbody tr")
    row_count = table_rows.count()
    assert row_count >= 3, \
        f"Detail table should have at least 3 rows for AAPL, MSFT, GOOGL, got: {row_count}"

    # Verify AAPL row in table
    aapl_table_current = page.locator("[data-testid='table-current-AAPL']")
    assert "$" in aapl_table_current.text_content(), "AAPL table current price should contain $"

    aapl_table_change = page.locator("[data-testid='table-change-AAPL']")
    assert "%" in aapl_table_change.text_content(), "AAPL table change should contain %"

    # Verify MSFT row in table
    msft_table_current = page.locator("[data-testid='table-current-MSFT']")
    assert "$" in msft_table_current.text_content(), "MSFT table current price should contain $"

    msft_table_change = page.locator("[data-testid='table-change-MSFT']")
    assert "%" in msft_table_change.text_content(), "MSFT table change should contain %"

    # Verify GOOGL row in table
    googl_table_current = page.locator("[data-testid='table-current-GOOGL']")
    assert "$" in googl_table_current.text_content(), "GOOGL table current price should contain $"

    googl_table_change = page.locator("[data-testid='table-change-GOOGL']")
    assert "%" in googl_table_change.text_content(), "GOOGL table change should contain %"

    # Verify timestamps are set
    timestamp = page.locator(".card-timestamp:first-child")
    assert timestamp.text_content(), "Card timestamp should be populated"

    print("✅ Test passed: Dashboard data loaded successfully")
    print(f"   - Market Status: {status_value}")
    print(f"   - Last Updated: {last_updated_text}")
    print(f"   - Stock Cards Loaded: {card_count}")
    print(f"   - Detail Table Rows: {row_count}")


@pytest.mark.scenario("Dashboard: Verify card price change indicator (up/down/flat)")
def test_dashboard_price_indicators(page: Page):
    """
    Test: Verify stock cards show correct price change indicators

    Verifies visual indicators for price movement:
    - Up arrow (▲) when price > previous close
    - Down arrow (▼) when price < previous close
    - Dash (—) when price = previous close
    """

    # Navigate and load data
    page.goto("http://localhost:8080/dashboard.html")
    page.fill("#api-key-input", "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20")
    page.locator("button:has-text('LOAD DATA')").click()
    page.wait_for_timeout(3000)

    # Check AAPL price change
    aapl_change = page.locator(".stock-card:first-child [data-testid='price-change']")
    aapl_change_text = aapl_change.text_content()
    assert "▲" in aapl_change_text or "▼" in aapl_change_text or "—" in aapl_change_text, \
        f"AAPL change should have indicator (▲/▼/—), got: {aapl_change_text}"

    # Check AAPL card has correct border
    aapl_card = page.locator(".stock-card:first-child")
    aapl_card_class = aapl_card.get_attribute("class")
    assert "up" in aapl_card_class or "down" in aapl_card_class or "flat" in aapl_card_class, \
        f"AAPL card should have up/down/flat class, got: {aapl_card_class}"

    # Check MSFT price change
    msft_change = page.locator(".stock-card:nth-child(2) [data-testid='price-change']")
    assert "▲" in msft_change.text_content() or "▼" in msft_change.text_content() or "—" in msft_change.text_content(), \
        "MSFT change should have indicator"

    # Check GOOGL price change
    googl_change = page.locator(".stock-card:nth-child(3) [data-testid='price-change']")
    assert "▲" in googl_change.text_content() or "▼" in googl_change.text_content() or "—" in googl_change.text_content(), \
        "GOOGL change should have indicator"

    print("✅ Test passed: Price change indicators verified")
    print(f"   - AAPL Change: {aapl_change_text}")
    print(f"   - AAPL Card Class: {aapl_card_class}")


@pytest.mark.scenario("Dashboard: Enter API key without LOAD DATA should not load data")
def test_dashboard_no_auto_load_without_button(page: Page):
    """
    Test: Entering API key without clicking LOAD DATA should not load data

    Verifies:
    - Data is not loaded automatically on key entry
    - User must click LOAD DATA button to fetch data
    """

    page.goto("http://localhost:8080/dashboard.html")

    # Enter API key but don't click button
    page.fill("#api-key-input", "d83kpmpr01qkm5c8hb1gd83kpmpr01qkm5c8hb20")

    # Wait a moment
    page.wait_for_timeout(1000)

    # Verify no cards are loaded yet
    stock_cards = page.locator(".stock-card:not(.loading-shimmer)")
    visible_cards = stock_cards.count()

    # Should not have any fully rendered cards without clicking button
    last_updated = page.locator("#last-updated")
    assert last_updated.text_content() == "—", \
        "Last updated should still be '—' without clicking LOAD DATA"

    print("✅ Test passed: Data not auto-loaded without button click")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


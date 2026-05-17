"""
Test scripts for validating application functionality.

Tests should use page objects from src/pages/ for page interactions.

Example:
    # src/tests/test_dashboard.py
    from src.pages.dashboard_page import DashboardPage

    @pytest.mark.scenario("Verify stock price displays correctly")
    async def test_stock_price_display(page, get_page_fixture):
        DashboardPage = get_page_fixture('dashboard_page.DashboardPage')
        dashboard = DashboardPage(page)
        price = dashboard.get_stock_price()
        assert price is not None
"""

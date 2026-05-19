import pytest
from src.utils.pages_loader import PageLoader
from src.api.finnhub_client import FinnhubClient


@pytest.mark.asyncio
class TestDashboardUI:
    @pytest.mark.scenario("Verify data is getting loaded in UI dashboard")
    async def test_ui_dashboard(self, async_page):
        pages = PageLoader(async_page)
        await pages.dashboard.enter_api_key()
        await pages.dashboard.click_load_button()
        await pages.dashboard.wait_for_data_load()
        await pages.dashboard.verify_dashboard_is_loaded()

    @pytest.mark.scenario("Verify stock card values are getting loaded in UI dashboard")
    async def test_stock_card_values_in_dashboard(self, async_page):
        pages = PageLoader(async_page)
        await pages.dashboard.enter_api_key()
        await pages.dashboard.click_load_button()
        await pages.dashboard.wait_for_data_load()
        card_values = await pages.dashboard.get_first_card_values()
        await pages.dashboard.verify_stock_card_details_are_loaded(card_values)

    @pytest.mark.scenario("Verify stock details grid values are same as stock card values loaded in UI dashboard")
    async def test_stock_details_grid_values_in_dashboard(self, async_page):
        pages = PageLoader(async_page)
        await pages.dashboard.enter_api_key()
        await pages.dashboard.click_load_button()
        await pages.dashboard.wait_for_data_load()
        await pages.dashboard.is_detail_section_visible()
        details_row_values = await pages.dashboard.get_first_details_row_values()
        await pages.dashboard.verify_details_row_values(details_row_values)

    @pytest.mark.scenario("Verify stock card data matches API response data")
    async def test_stock_card_data_matches_api_response(self, async_page):
        pages = PageLoader(async_page)
        await pages.dashboard.enter_api_key()
        await pages.dashboard.click_load_button()
        await pages.dashboard.wait_for_data_load()
        card_data = await pages.dashboard.get_card_data_for_api_comparison()
        finnhub = FinnhubClient()
        api_response = finnhub.get_quote(card_data["symbol"])
        await pages.dashboard.compare_card_data_with_api(card_data, api_response)

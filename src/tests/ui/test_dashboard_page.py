import pytest
from src.utils.pages_loader import PageLoader


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

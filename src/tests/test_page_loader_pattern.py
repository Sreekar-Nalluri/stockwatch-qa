import pytest
from src.utils.pages_loader import PageLoader


@pytest.mark.asyncio
@pytest.mark.scenario("Verify stock data is getting loaded in UI dashboard")
async def test_dashboard_with_page_loader(async_page):
    pages = PageLoader(async_page)
    await pages.dashboard.enter_api_key()
    await pages.dashboard.click_load_button()
    await pages.dashboard.wait_for_data_load()
    await pages.dashboard.complete_ui_workflow()

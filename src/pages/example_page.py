"""
Example Page Object Model class.

This demonstrates the structure of a page helper class that the PageLoader
can discover and load. You can use this as a template for creating your own
page objects.

Replace the locators and methods with those specific to your application.
"""

from playwright.async_api import Page


class ExamplePage:
    """Example page object for the dashboard."""

    def __init__(self, page: Page):
        """
        Initialize the page object.

        Args:
            page: Playwright async Page instance
        """
        self.page = page
        self.header_title = page.locator("h1.header-title")
        self.search_input = page.locator("input[data-testid='search-input']")
        self.submit_button = page.locator("button[data-testid='submit-btn']")
        self.results_container = page.locator("div[data-testid='results']")

    # ========================
    # Action Methods
    # ========================

    async def get_page_title(self) -> str:
        """Get the page title."""
        return await self.page.title()

    async def get_header_text(self) -> str:
        """Get the header text."""
        return await self.header_title.text_content()

    async def fill_search_input(self, text: str) -> None:
        """
        Fill the search input with text.

        Args:
            text: Text to enter in search input
        """
        await self.search_input.fill(text)

    async def click_submit_button(self) -> None:
        """Click the submit button."""
        await self.submit_button.click()

    async def search_for(self, text: str) -> None:
        """
        Perform a search action.

        Args:
            text: Search term
        """
        await self.fill_search_input(text)
        await self.click_submit_button()

    async def get_results_count(self) -> int:
        """Get the number of results displayed."""
        results = await self.results_container.locator("div").count()
        return results

    async def wait_for_results(self, timeout: int = 5000) -> bool:
        """
        Wait for results to appear.

        Args:
            timeout: Timeout in milliseconds

        Returns:
            True if results appear, False otherwise
        """
        try:
            await self.results_container.wait_for(timeout=timeout)
            return True
        except Exception:
            return False

"""
Example Page Object Model class.

This demonstrates the structure of a page helper class that the PageLoader
can discover and load. You can use this as a template for creating your own
page objects.

Replace the locators and methods with those specific to your application.
"""

from playwright.sync_api import Page


class ExamplePage:
    """Example page object for the dashboard."""

    def __init__(self, page: Page):
        """
        Initialize the page object.

        Args:
            page: Playwright Page instance
        """
        self.page = page

    # ========================
    # Locators (as properties)
    # ========================

    @property
    def header_title(self) -> str:
        """Header title locator."""
        return "//h1[@class='header-title']"

    @property
    def search_input(self) -> str:
        """Search input field locator."""
        return "input[data-testid='search-input']"

    @property
    def submit_button(self) -> str:
        """Submit button locator."""
        return "button[data-testid='submit-btn']"

    @property
    def results_container(self) -> str:
        """Results container locator."""
        return "div[data-testid='results']"

    # ========================
    # Action Methods
    # ========================

    def get_page_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def get_header_text(self) -> str:
        """Get the header text."""
        return self.page.text_content(self.header_title)

    def fill_search_input(self, text: str) -> None:
        """
        Fill the search input with text.

        Args:
            text: Text to enter in search input
        """
        self.page.fill(self.search_input, text)

    def click_submit_button(self) -> None:
        """Click the submit button."""
        self.page.click(self.submit_button)

    def search_for(self, text: str) -> None:
        """
        Perform a search action.

        Args:
            text: Search term
        """
        self.fill_search_input(text)
        self.click_submit_button()

    def get_results_count(self) -> int:
        """Get the number of results displayed."""
        results = self.page.query_selector_all(self.results_container)
        return len(results)

    def wait_for_results(self, timeout: int = 5000) -> bool:
        """
        Wait for results to appear.

        Args:
            timeout: Timeout in milliseconds

        Returns:
            True if results appear, False otherwise
        """
        try:
            self.page.wait_for_selector(self.results_container, timeout=timeout)
            return True
        except Exception:
            return False


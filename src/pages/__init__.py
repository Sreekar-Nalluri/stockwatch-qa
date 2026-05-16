"""
Page objects for UI automation.

Page helper classes should be defined in this folder.
Each page helper file contains a class with locators and action methods.

Example:
    # src/pages/dashboard_page.py
    from playwright.sync_api import Page

    class DashboardPage:
        def __init__(self, page: Page):
            self.page = page

        # Locators
        @property
        def stock_price_locator(self):
            return "h1[data-testid='stock-price']"

        # Action methods
        def get_stock_price(self) -> str:
            return self.page.text_content(self.stock_price_locator)
"""


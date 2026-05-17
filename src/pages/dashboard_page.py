from playwright.async_api import Page
from conftest import env_config


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

        # ===== HEADER & STATUS LOCATORS =====
        self.status_dot = page.locator("#status-dot")
        self.status_text = page.locator("#status-text")

        # ===== API KEY BANNER LOCATORS =====
        self.api_key_input = page.locator("#api-key-input")
        self.load_button = page.locator("button:has-text('LOAD DATA')")

        # ===== ERROR MESSAGE LOCATORS =====
        self.error_msg = page.locator("#error-msg")
        self.error_msg_element = page.locator(".error-msg")

        # ===== SEARCH/SYMBOL LOCATORS =====
        self.symbol_input = page.locator("#symbol-input")
        self.add_symbol_button = page.locator("button:has-text('ADD')")
        self.quick_symbols = page.locator(".quick-symbols")

        # ===== REFRESH BAR LOCATORS =====
        self.last_updated = page.locator("#last-updated")
        self.refresh_button = page.locator("button:has-text('↻ REFRESH')")

        # ===== CARDS GRID LOCATORS =====
        self.cards_grid = page.locator("#cards-grid")
        self.stock_cards = page.locator(".stock-card")
        self.stock_cards_loading = page.locator(".stock-card.loading-shimmer")

        # ===== DETAIL TABLE LOCATORS =====
        self.detail_section = page.locator("#detail-section")
        self.detail_tbody = page.locator("#detail-tbody")
        self.detail_rows = page.locator("tbody tr")


    async def enter_api_key(self) -> None:
        api_key = env_config.finnhub_key()
        await self.api_key_input.fill(api_key)

    async def click_load_button(self) -> None:
        await self.load_button.click()

    async def wait_for_data_load(self, timeout: int = 5000) -> None:
        await self.page.wait_for_timeout(timeout)
        print(f"[OK] Waited {timeout}ms for data to load")

    async def get_market_status(self) -> str:
        """Get the current market status text.

        Returns:
            Market status text (e.g., "MARKET OPEN", "MARKET CLOSED")
        """
        text = await self.status_text.text_content()
        return text.strip() if text else ""

    async def get_status_dot_class(self) -> str:
        """Get the status dot CSS classes.

        Returns:
            CSS class string (should contain 'open' or 'closed')
        """
        css_class = await self.status_dot.get_attribute("class")
        return css_class or ""

    async def is_status_open(self) -> bool:
        """Check if market status is OPEN.

        Returns:
            True if market is open, False otherwise
        """
        status = await self.get_market_status()
        return "OPEN" in status

    # ===== ERROR HANDLING METHODS =====

    async def get_error_message(self) -> str:
        if await self.error_msg_element.is_visible():
            text = await self.error_msg_element.text_content()
            return text.strip() if text else ""
        return ""

    async def is_error_visible(self) -> bool:
        return await self.error_msg_element.is_visible()

    async def clear_error(self) -> None:
        await self.error_msg_element.evaluate("el => el.style.display = 'none'")

    # ===== STOCK DATA VERIFICATION METHODS =====

    async def get_last_updated(self) -> str:
        text = await self.last_updated.text_content()
        return text.strip() if text else ""

    async def get_stock_cards_count(self) -> int:
        count = await self.stock_cards.count()
        return count

    async def is_loading(self) -> bool:
        """Check if loading shimmer is visible.

        Returns:
            True if loading animation is showing
        """
        count = await self.stock_cards_loading.count()
        return count > 0

    async def get_first_card_symbol(self) -> str:
        symbol_locator = self.page.locator(".stock-card:first-child [data-testid='symbol']")
        text = await symbol_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_price(self) -> str:
        price_locator = self.page.locator(".stock-card:first-child [data-testid='current-price']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_change(self) -> str:
        change_locator = self.page.locator(".stock-card:first-child [data-testid='price-change']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_open_price(self) -> str:
        open_locator = self.page.locator(".stock-card:first-child [data-testid='open-price']")
        text = await open_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_high_price(self) -> str:
        high_locator = self.page.locator(".stock-card:first-child [data-testid='day-high']")
        text = await high_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_low_price(self) -> str:
        low_locator = self.page.locator(".stock-card:first-child [data-testid='day-low']")
        text = await low_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_prev_close(self) -> str:
        prev_close_locator = self.page.locator(".stock-card:first-child [data-testid='prev-close']")
        text = await prev_close_locator.text_content()
        return text.strip() if text else ""

    async def get_nth_card_symbol(self, index: int) -> str:
        symbol_locator = self.page.locator(f".stock-card:nth-child({index}) [data-testid='symbol']")
        text = await symbol_locator.text_content()
        return text.strip() if text else ""

    async def get_nth_card_price(self, index: int) -> str:
        price_locator = self.page.locator(f".stock-card:nth-child({index}) [data-testid='current-price']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_nth_card_change(self, index: int) -> str:
        change_locator = self.page.locator(f".stock-card:nth-child({index}) [data-testid='price-change']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_detail_table_rows_count(self) -> int:
        count = await self.detail_rows.count()
        return count

    async def is_detail_section_visible(self) -> bool:
        return await self.detail_section.is_visible()

    async def get_table_cell_value(self, row_index: int, column_index: int) -> str:
        cell = self.page.locator(f"tbody tr:nth-child({row_index + 1}) td:nth-child({column_index + 1})")
        text = await cell.text_content()
        return text.strip() if text else ""

    async def get_aapl_table_current_price(self) -> str:
        price_locator = self.page.locator("[data-testid='table-current-AAPL']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_aapl_table_change(self) -> str:
        change_locator = self.page.locator("[data-testid='table-change-AAPL']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_msft_table_current_price(self) -> str:
        price_locator = self.page.locator("[data-testid='table-current-MSFT']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_msft_table_change(self) -> str:
        change_locator = self.page.locator("[data-testid='table-change-MSFT']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_googl_table_current_price(self) -> str:
        price_locator = self.page.locator("[data-testid='table-current-GOOGL']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_googl_table_change(self) -> str:
        change_locator = self.page.locator("[data-testid='table-change-GOOGL']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def verify_data_loaded(self) -> bool:
        """Verify that data has been successfully loaded.

        Returns:
            True if data is loaded, False otherwise
        """
        # Check if market status is set
        status = await self.get_market_status()
        if not status or status == "checking...":
            return False

        # Check if last updated is set
        last_updated = await self.get_last_updated()
        if not last_updated or last_updated == "—":
            return False

        # Check if cards are loaded
        cards_count = await self.get_stock_cards_count()
        if cards_count == 0:
            return False

        return True

    async def complete_ui_workflow(self):
        market_status = await self.get_market_status()
        last_updated = await self.get_last_updated()
        cards_count = await self.get_stock_cards_count()
        table_rows = await self.get_detail_table_rows_count()
        aapl_price = await self.get_first_card_price()
            
        is_valid = (
            market_status in ["MARKET OPEN", "MARKET CLOSED"] and
            last_updated != "—" and
            cards_count >= 3 and
            table_rows >= 3 and
            "$" in aapl_price
        )
        assert is_valid, f"Workflow failed"
        assert cards_count >= 3, f"Need at least 3 cards, got: {cards_count}"

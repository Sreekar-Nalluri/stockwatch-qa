from playwright.async_api import Page


class DashboardPage:
    """Page Object for Stock Dashboard

    Encapsulates all locators and interactions with the dashboard UI.
    All methods are async to support Playwright async API.
    """

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

    # ===== API KEY & LOAD METHODS =====

    async def enter_api_key(self, api_key: str) -> None:
        """Enter API key in the input field.

        Args:
            api_key: The Finnhub API key to enter
        """
        await self.api_key_input.fill(api_key)
        print(f"[OK] Entered API key")

    async def click_load_button(self) -> None:
        """Click the LOAD DATA button to fetch stock data."""
        await self.load_button.click()
        print(f"[OK] Clicked LOAD DATA button")

    async def wait_for_data_load(self, timeout: int = 5000) -> None:
        """Wait for data to load.
        
        Args:
            timeout: Timeout in milliseconds
        """
        await self.page.wait_for_timeout(timeout)
        print(f"[OK] Waited {timeout}ms for data to load")

    # ===== STATUS VERIFICATION METHODS =====

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
        """Get error message text if displayed.

        Returns:
            Error message text or empty string if not visible
        """
        if await self.error_msg_element.is_visible():
            text = await self.error_msg_element.text_content()
            return text.strip() if text else ""
        return ""

    async def is_error_visible(self) -> bool:
        """Check if error message is visible.
        
        Returns:
            True if error message is displayed
        """
        return await self.error_msg_element.is_visible()

    async def clear_error(self) -> None:
        """Clear/hide the error message."""
        await self.error_msg_element.evaluate("el => el.style.display = 'none'")
        print(f"[OK] Cleared error message")

    # ===== STOCK DATA VERIFICATION METHODS =====

    async def get_last_updated(self) -> str:
        """Get the last updated timestamp.

        Returns:
            Last updated text (e.g., "12:34:56 PM") or "—" if not updated
        """
        text = await self.last_updated.text_content()
        return text.strip() if text else ""

    async def get_stock_cards_count(self) -> int:
        """Get the number of stock cards loaded.

        Returns:
            Number of stock cards
        """
        count = await self.stock_cards.count()
        return count

    async def is_loading(self) -> bool:
        """Check if loading shimmer is visible.
        
        Returns:
            True if loading animation is showing
        """
        count = await self.stock_cards_loading.count()
        return count > 0

    # ===== FIRST STOCK CARD (AAPL) METHODS =====

    async def get_first_card_symbol(self) -> str:
        """Get symbol from first stock card.

        Returns:
            Stock symbol (e.g., "AAPL")
        """
        symbol_locator = self.page.locator(".stock-card:first-child [data-testid='symbol']")
        text = await symbol_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_price(self) -> str:
        """Get current price from first stock card.

        Returns:
            Price text (e.g., "$150.25")
        """
        price_locator = self.page.locator(".stock-card:first-child [data-testid='current-price']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_change(self) -> str:
        """Get price change from first stock card.

        Returns:
            Change text with indicator (e.g., "▲ +5.50 (+3.80%)")
        """
        change_locator = self.page.locator(".stock-card:first-child [data-testid='price-change']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_open_price(self) -> str:
        """Get open price from first stock card.

        Returns:
            Open price text (e.g., "$148.50")
        """
        open_locator = self.page.locator(".stock-card:first-child [data-testid='open-price']")
        text = await open_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_high_price(self) -> str:
        """Get day high price from first stock card.

        Returns:
            Day high price text (e.g., "$152.75")
        """
        high_locator = self.page.locator(".stock-card:first-child [data-testid='day-high']")
        text = await high_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_low_price(self) -> str:
        """Get day low price from first stock card.

        Returns:
            Day low price text (e.g., "$148.25")
        """
        low_locator = self.page.locator(".stock-card:first-child [data-testid='day-low']")
        text = await low_locator.text_content()
        return text.strip() if text else ""

    async def get_first_card_prev_close(self) -> str:
        """Get previous close price from first stock card.

        Returns:
            Previous close price text (e.g., "$149.75")
        """
        prev_close_locator = self.page.locator(".stock-card:first-child [data-testid='prev-close']")
        text = await prev_close_locator.text_content()
        return text.strip() if text else ""

    # ===== NTH STOCK CARD METHODS =====

    async def get_nth_card_symbol(self, index: int) -> str:
        """Get symbol from nth stock card (1-indexed).

        Args:
            index: Card index (1-indexed, e.g., 1 for first, 2 for second)

        Returns:
            Stock symbol
        """
        symbol_locator = self.page.locator(f".stock-card:nth-child({index}) [data-testid='symbol']")
        text = await symbol_locator.text_content()
        return text.strip() if text else ""

    async def get_nth_card_price(self, index: int) -> str:
        """Get current price from nth stock card.

        Args:
            index: Card index (1-indexed)

        Returns:
            Price text
        """
        price_locator = self.page.locator(f".stock-card:nth-child({index}) [data-testid='current-price']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_nth_card_change(self, index: int) -> str:
        """Get price change from nth stock card.

        Args:
            index: Card index (1-indexed)

        Returns:
            Change text
        """
        change_locator = self.page.locator(f".stock-card:nth-child({index}) [data-testid='price-change']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    # ===== DETAIL TABLE METHODS =====

    async def get_detail_table_rows_count(self) -> int:
        """Get number of rows in detail table.

        Returns:
            Number of table rows
        """
        count = await self.detail_rows.count()
        return count

    async def is_detail_section_visible(self) -> bool:
        """Check if detail section is visible.

        Returns:
            True if detail section is displayed
        """
        return await self.detail_section.is_visible()

    async def get_table_cell_value(self, row_index: int, column_index: int) -> str:
        """Get value from table cell.

        Args:
            row_index: Row index (0-indexed)
            column_index: Column index (0-indexed)
        
        Returns:
            Cell text value
        """
        cell = self.page.locator(f"tbody tr:nth-child({row_index + 1}) td:nth-child({column_index + 1})")
        text = await cell.text_content()
        return text.strip() if text else ""

    async def get_aapl_table_current_price(self) -> str:
        """Get AAPL current price from detail table.

        Returns:
            Current price text
        """
        price_locator = self.page.locator("[data-testid='table-current-AAPL']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_aapl_table_change(self) -> str:
        """Get AAPL price change from detail table.

        Returns:
            Change percentage text
        """
        change_locator = self.page.locator("[data-testid='table-change-AAPL']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_msft_table_current_price(self) -> str:
        """Get MSFT current price from detail table."""
        price_locator = self.page.locator("[data-testid='table-current-MSFT']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_msft_table_change(self) -> str:
        """Get MSFT price change from detail table."""
        change_locator = self.page.locator("[data-testid='table-change-MSFT']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    async def get_googl_table_current_price(self) -> str:
        """Get GOOGL current price from detail table."""
        price_locator = self.page.locator("[data-testid='table-current-GOOGL']")
        text = await price_locator.text_content()
        return text.strip() if text else ""

    async def get_googl_table_change(self) -> str:
        """Get GOOGL price change from detail table."""
        change_locator = self.page.locator("[data-testid='table-change-GOOGL']")
        text = await change_locator.text_content()
        return text.strip() if text else ""

    # ===== WORKFLOW METHODS =====

    async def load_data_with_key(self, api_key: str) -> None:
        """Complete workflow: enter API key and load data.

        Args:
            api_key: The Finnhub API key
        """
        await self.enter_api_key(api_key)
        await self.click_load_button()
        print(f"[OK] Loaded data with API key (first 10 chars): {api_key[:10]}...")

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

    async def complete_ui_workflow(self, api_key: str, wait_time: int = 5000) -> dict:
        """
        Complete UI workflow in one async call:
        1. Enter API key
        2. Click LOAD DATA button
        3. Wait for data
        4. Verify and collect data
        
        Args:
            api_key: Finnhub API key
            wait_time: Milliseconds to wait for data load (default 5000)
        
        Returns:
            Dictionary with verification results:
            {
                'success': bool,
                'market_status': str,
                'last_updated': str,
                'cards_count': int,
                'table_rows': int,
                'aapl_price': str,
                'error': str or None
            }
        """
        try:
            await self.enter_api_key(api_key)
            await self.click_load_button()
            await self.wait_for_data_load(timeout=wait_time)
            
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

            return {
                'success': is_valid,
                'market_status': market_status,
                'last_updated': last_updated,
                'cards_count': cards_count,
                'table_rows': table_rows,
                'aapl_price': aapl_price,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'market_status': '',
                'last_updated': '',
                'cards_count': 0,
                'table_rows': 0,
                'aapl_price': '',
                'error': str(e)
            }

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

        # Card details locators
        self.card_values_locators = {"time_stamp": "timestamp",
                                     "symbol": "symbol",
                                     "current_price": "current-price",
                                     "price_change": "price-change",
                                     "open_price": "open-price",
                                     "prev_close": "prev-close",
                                     "day_high": "day-high",
                                     "day_low": "day-low"}
        self.card_label = ".card-label"

        # ===== DETAIL TABLE LOCATORS =====
        self.detail_section = page.locator("#detail-section")
        self.detail_tbody = page.locator("#detail-tbody")
        self.detail_rows = page.locator("tbody tr")
        self.details_section = {"symbol": ".td-sym",
                                "current_price": "td:nth-child(2)",
                                "open_price": "td:nth-child(3)",
                                "day_high": "td:nth-child(4)",
                                "day_low": "td:nth-child(5)",
                                "prev_close": "td:nth-child(6)",
                                "price_change": "td:nth-child(7)",
                                "time_stamp": "td:last-child"}

    async def enter_api_key(self) -> None:
        api_key = env_config.finnhub_key()
        await self.api_key_input.fill(api_key)

    async def click_load_button(self) -> None:
        await self.load_button.click()

    async def wait_for_data_load(self, timeout: int = 5000) -> None:
        await self.page.wait_for_timeout(timeout)

    async def get_market_status(self) -> str:
        """Get the current market status text.

        Returns:
            Market status text (e.g., "MARKET OPEN", "MARKET CLOSED")
        """
        text = await self.status_text.text_content()
        return text.strip() if text else ""

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

    async def get_first_card_values(self) -> dict:
        card_values = {}
        for key, value in self.card_values_locators.items():
            card_values[key] = await self.stock_cards.first.get_by_test_id(value).text_content()
        card_values["label"] = await self.stock_cards.first.locator(self.card_label).text_content()
        assert card_values, "no values found in card"
        return card_values

    async def get_first_details_row_values(self) -> dict:
        details = {}
        for key, value in self.details_section.items():
            details[key] = await self.detail_rows.first.locator(value).text_content()
        return details

    async def get_first_card_price(self):
        return await self.stock_cards.first.get_by_test_id('current-price').text_content()

    async def get_detail_table_rows_count(self) -> int:
        count = await self.detail_rows.count()
        return count

    async def is_detail_section_visible(self):
        assert await self.detail_section.is_visible(), "details section not loaded"

    async def verify_dashboard_is_loaded(self):
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
        assert is_valid, "Dashboard failed to load"
        assert cards_count >= 3, f"Need at least 3 cards, got: {cards_count}"

    @staticmethod
    async def verify_stock_card_details_are_loaded(card_details):
        assert card_details["symbol"] == "AAPL", f"AAPL symbol not found, got {card_details['symbol']}"
        assert card_details["time_stamp"], f"Time stamp not found, got {card_details['time_stamp']}"
        assert card_details["label"] == "NYSE / NASDAQ", f"NYSE / NASDAQ label not found: {card_details['label']}"
        assert card_details["current_price"], f"Price should contain $ with value, got {card_details['current_price']}"
        assert card_details["price_change"], f"Price change should be displayed, got {card_details['price_change']}"
        assert "▲" in card_details["price_change"] or "▼" in card_details["price_change"] or "—" in card_details["price_change"], \
            f"should have indicator (▲/▼/—), got {card_details['price_change']}"
        assert card_details["open_price"], f"Open price should contain $ with value, got {card_details['open_price']}"
        assert card_details["prev_close"], f"Previous close price should contain $ with value, got {card_details['prev_close']}"
        assert card_details["day_high"], f"Day high should contain $ with value, got {card_details['day_high']}"
        assert card_details["day_low"], f"Day low should contain $ with value, got {card_details['day-low']}"

    async def verify_details_row_values(self, details_row):
        table_rows = await self.get_detail_table_rows_count()
        card_values = await self.get_first_card_values()
        assert table_rows >= 3, f"Detail table should have at least 3 rows, got: {table_rows}"
        for key, value in details_row.items():
            if key == "price_change":
                assert details_row[key] in card_values[key], \
                    f"Price change in details {details_row[key]} not equal to card value {card_values[key]}"
            else:
                assert details_row[key] == card_values[key], \
                    f"card value {card_values[key]} not equal to details row value {details_row[key]}"

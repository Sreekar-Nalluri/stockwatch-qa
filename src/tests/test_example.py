"""
Example test file demonstrating how to use page objects with the PageLoader.

This shows the recommended structure for your tests.
You can delete this file once you understand the pattern and create your own tests.
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.scenario("Example: Load and use page object with PageLoader")
def test_page_object_loading(page: Page, get_page_fixture):
    """
    Example test showing how to dynamically load and use a page object.

    Args:
        page: Pytest fixture providing Playwright Page instance
        get_page_fixture: Fixture that provides access to PageLoader.get_page()
    """
    # Load the page object class dynamically
    ExamplePage = get_page_fixture('example_page.ExamplePage')

    # Navigate to your application
    page.goto("http://localhost:8080/dashboard.html")

    # Initialize the page object with the page instance
    example_page = ExamplePage(page)

    # Use the page object methods
    title = example_page.get_page_title()
    assert title is not None

    print(f"✓ Page title: {title}")


@pytest.mark.scenario("Example: Direct page object import")
def test_direct_page_import(page: Page):
    """
    Example test showing direct import of page object.
    Use this approach if you prefer static imports.

    Args:
        page: Pytest fixture providing Playwright Page instance
    """
    from src.pages.example_page import ExamplePage

    # Navigate to your application
    page.goto("http://localhost:8080/dashboard.html")

    # Initialize and use the page object
    example_page = ExamplePage(page)
    title = example_page.get_page_title()

    print(f"✓ Page title: {title}")


@pytest.mark.scenario("Example: Load all available page objects")
def test_load_all_pages(pages_loader):
    """
    Example showing how to discover and load all page objects at once.

    Args:
        pages_loader: Fixture providing access to PageLoader utility
    """
    # Load all page objects from pages folder
    all_pages = pages_loader.load_all_pages()

    print(f"✓ Found {len(all_pages)} page object(s):")
    for name, page_class in all_pages.items():
        print(f"  - {name}: {page_class}")

    assert len(all_pages) > 0, "Should find at least one page object"


@pytest.mark.scenario("Example: Use environment variables")
def test_environment_variables(get_page_fixture):
    """
    Example showing how to access environment variables
    that were loaded by EnvConfig.

    Args:
        get_page_fixture: Fixture providing access to PageLoader
    """
    from src.utils.env_config import EnvConfig

    # Get environment variables with defaults
    base_url = EnvConfig.get("BASE_URL", "http://localhost:8080")
    symbol = EnvConfig.get("SYMBOL", "AAPL")

    print(f"✓ BASE_URL: {base_url}")
    print(f"✓ SYMBOL: {symbol}")

    assert base_url is not None
    assert symbol == "AAPL"  # Default we set


@pytest.mark.scenario("Example: Get required environment variable")
def test_required_environment_variable():
    """
    Example showing error handling when required environment variables
    are not found.
    """
    from config import EnvConfig

    try:
        # This will succeed if FINNHUB_KEY is set
        api_key = EnvConfig.get_required("FINNHUB_KEY")
        print("✓ FINNHUB_KEY is configured")
        assert api_key is not None
    except ValueError as e:
        # This would be raised if FINNHUB_KEY is not in runtime env,
        # config/.env, or config/.env.local
        print(f"⚠ {e}")
        pytest.skip("FINNHUB_KEY not configured")

"""
Example tests demonstrating the new unified fixtures system.

This shows how to use the enhanced fixtures that:
1. Load all pages at once (all_pages fixture)
2. Support runtime browser selection
3. Include automatic BASE_URL navigation and Finnhub API connection
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.scenario("Unified: Use test_context with all pages and API")
def test_with_unified_context(test_context):
    """
    Example using the unified test_context fixture.

    This fixture provides:
    - page: Browser page instance (already navigated to BASE_URL)
    - pages: All loaded page objects
    - api: Finnhub API request context
    - config: Configuration (BASE_URL, FINNHUB_KEY, SYMBOL)

    Args:
        test_context: Unified fixture providing complete test context
    """
    page = test_context['page']
    pages = test_context['pages']
    api = test_context['api']
    config = test_context['config']

    # Page should be loaded
    assert page is not None

    # All pages should be loaded
    print(f"✓ Available pages: {list(pages.keys())}")
    assert len(pages) > 0, "Should have at least one page object"

    # Config should be available
    assert config['base_url'] is not None
    assert config['symbol'] == 'AAPL'

    print(f"✓ Test context is ready:")
    print(f"  - Base URL: {config['base_url']}")
    print(f"  - Symbol: {config['symbol']}")
    print(f"  - Pages loaded: {len(pages)}")


@pytest.mark.scenario("Unified: Load all pages and use with page")
def test_load_all_pages_direct(page_with_url, all_pages):
    """
    Example showing direct usage of all_pages fixture.

    Args:
        page_with_url: Page instance already navigated to BASE_URL
        all_pages: Dictionary of all loaded page objects
    """
    # Page should be at BASE_URL
    assert page_with_url is not None

    # All pages should be loaded
    print(f"✓ Loaded page objects:")
    for page_name, page_class in all_pages.items():
        print(f"  - {page_name}: {page_class}")
        # Initialize each page object
        page_obj = page_class(page_with_url)
        assert page_obj is not None

    assert len(all_pages) > 0


@pytest.mark.scenario("Unified: Test API with Finnhub data")
def test_api_price_data(api_price):
    """
    Example showing how to use API fixture to get stock data.

    Args:
        api_price: Stock quote data fetched from Finnhub
    """
    if api_price:
        print(f"✓ Stock price data received:")
        for key, value in api_price.items():
            print(f"  - {key}: {value}")

        # Verify expected keys exist
        assert 'c' in api_price or len(api_price) == 0, "Should have current price or be empty"
    else:
        print("⚠️  No API data available (may not be configured)")


@pytest.mark.scenario("Unified: Browser type selection at runtime")
def test_browser_type_detection(browser, browser_name):
    """
    Example showing runtime browser type selection.

    Run with: pytest --browser=firefox or pytest --browser=webkit

    Args:
        browser: Launched browser instance
        browser_name: Selected browser type (from fixture)
    """
    assert browser is not None
    print(f"✓ Browser type: {browser_name}")
    print(f"✓ Browser instance: {browser}")

    # Verify browser type matches
    assert browser_name in ["chromium", "firefox", "webkit"]


@pytest.mark.scenario("Old API: Still works - page object loading method")
def test_backward_compatibility_page_loader(page, get_page_fixture):
    """
    Backward compatibility test - old method still works.

    This shows that the previous fixture-based approach still works.

    Args:
        page: Playwright page instance
        get_page_fixture: Fixture for loading individual page classes
    """
    # Load a specific page object
    ExamplePage = get_page_fixture('example_page.ExamplePage')

    # Navigate to dashboard
    page.goto("http://localhost:8080/dashboard.html")

    # Create page object
    example_page = ExamplePage(page)

    # Use page object methods
    title = example_page.get_page_title()
    assert title is not None
    print(f"✓ Page title: {title}")


@pytest.mark.scenario("Old API: Still works - pages_loader fixture")
def test_backward_compatibility_pages_loader(pages_loader):
    """
    Backward compatibility test - old pages_loader fixture still works.

    Args:
        pages_loader: Fixture providing PageLoader utility
    """
    # Load all pages using the utility
    all_pages = pages_loader.load_all_pages()

    print(f"✓ Loaded {len(all_pages)} page(s) with pages_loader fixture:")
    for name, page_class in all_pages.items():
        print(f"  - {name}: {page_class}")

    assert len(all_pages) > 0


@pytest.mark.scenario("Advanced: Multiple pages at once for complex tests")
def test_complex_workflow_with_multiple_pages(test_context):
    """
    Example showing how to work with multiple page objects in a complex workflow.

    This demonstrates:
    1. Using multiple page objects in a single test
    2. Accessing API context
    3. Getting configuration

    Args:
        test_context: Unified fixture
    """
    page = test_context['page']
    pages = test_context['pages']
    api = test_context['api']
    config = test_context['config']

    # Get the first page object available
    if pages:
        page_class_name = list(pages.keys())[0]
        PageClass = pages[page_class_name]
        page_obj = PageClass(page)

        print(f"✓ Created instance of {page_class_name}")
        print(f"  - Class: {PageClass}")
        print(f"  - Instance: {page_obj}")

        # You could now use API context to fetch data
        print(f"✓ API context ready for {config['symbol']}")

        # And interact with the page object
        try:
            title = page.title()
            print(f"✓ Page title: {title}")
        except Exception as e:
            print(f"⚠️  Could not get title: {e}")


import pytest
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from playwright.sync_api import Page, APIRequestContext, Playwright, Browser, BrowserContext
import subprocess, time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import custom config loader
from utils.config import EnvConfig
from utils.pages_loader import PageLoader, get_page, load_all_pages

# Initialize environment variable loading
env_config = EnvConfig()

# Load configuration variables with fallback strategy
FINNHUB_KEY = EnvConfig.get("FINNHUB_KEY")
BASE_URL = EnvConfig.get("BASE_URL", "http://localhost:8080/dashboard.html")
SYMBOL = EnvConfig.get("SYMBOL", "AAPL")  # Default to AAPL if not specified
BROWSER_TYPE = EnvConfig.get("BROWSER_TYPE", "chromium")  # Default browser type


def pytest_addoption(parser):
    """Add command-line options for pytest."""
    # Note: --browser option is already provided by pytest-playwright
    # We only add --browser-channel if it doesn't exist
    try:
        parser.getgroup("playwright").addoption(
            "--browser-channel",
            action="store",
            default=None,
            help="Browser channel to use (e.g., msedge, chromium)"
        )
    except (ValueError, AttributeError):
        # Option might already exist or group doesn't exist, that's okay
        pass

@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Start HTTP server for dashboard.html"""
    # Find the dashboard directory
    project_root = Path(__file__).parent
    dashboard_dir = project_root / "dashboard"

    # If dashboard dir doesn't exist, just serve from project root
    if not dashboard_dir.exists():
        dashboard_dir = project_root
        print(f"ℹ Dashboard directory not found, using project root: {project_root}")
    else:
        print(f"ℹ Starting HTTP server in: {dashboard_dir}")

    try:
        proc = subprocess.Popen(
            ["python", "-m", "http.server", "8080"],
            cwd=str(dashboard_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)  # Let it start
        yield
        proc.terminate()
    except Exception as e:
        print(f"⚠️  Failed to start HTTP server: {e}")
        yield

@pytest.fixture(scope="session")
def finnhub_request(playwright: Playwright) -> APIRequestContext:
    """
    Fixture providing API request context for Finnhub API.

    Creates a session-scoped API context that points to Finnhub API
    with the authentication token included in headers.

    Returns:
        APIRequestContext configured for Finnhub API
    """
    # Use Finnhub API base URL
    finnhub_api_url = "https://finnhub.io/api/v1"

    if not FINNHUB_KEY:
        print("⚠️  WARNING: FINNHUB_KEY not configured. API calls will fail without authentication.")

    print(f"📡 Creating Finnhub API context at: {finnhub_api_url}")

    context = playwright.request.new_context(
        base_url=finnhub_api_url,
        extra_http_headers={"X-Finnhub-Token": FINNHUB_KEY} if FINNHUB_KEY else {}
    )
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def api_price(finnhub_request: APIRequestContext) -> dict:
    """
    Fixture to fetch stock quote data from Finnhub API.

    Fetches the stock price data once per session and reuses it across all tests.

    Returns:
        Dictionary containing stock quote data:
        - c: current price
        - h: high price
        - l: low price
        - o: open price
        - pc: previous close price
        - t: timestamp
    """
    try:
        print(f"📊 Fetching quote for symbol: {SYMBOL}")
        response = finnhub_request.get(f"/quote?symbol={SYMBOL}")

        if not response.ok:
            print(f"⚠️  API Error: {response.status} - {response.text}")
            return {}

        data = response.json()
        print(f"✓ Quote fetched successfully for {SYMBOL}: ${data.get('c', 'N/A')}")
        return data
    except Exception as e:
        print(f"❌ Error fetching quote: {e}")
        return {}

@pytest.fixture
def browser_name(request):
    """Get browser type from command-line option or environment variable."""
    try:
        browser_opt = request.config.getoption("--browser")
    except Exception:
        browser_opt = None

    # Priority: command-line option > environment variable > default
    browser = browser_opt or BROWSER_TYPE or "chromium"

    if not browser or (isinstance(browser, str) and browser.strip() == ""):
        browser = "chromium"

    if browser not in ["chromium", "firefox", "webkit"]:
        raise ValueError(
            f"Unsupported browser: {browser}. Use 'chromium', 'firefox', or 'webkit'."
        )

    return browser


@pytest.fixture
def browser_channel(request):
    """Get browser channel from command-line option."""
    try:
        return request.config.getoption("--browser-channel", default=None)
    except Exception:
        return None


@pytest.fixture
async def browser(browser_name, browser_channel):
    """Launch browser with specified type and channel."""
    print(f"🔍 Launching browser: {browser_name} (headless={check_headless_mode()})")

    async with async_playwright() as p:
        if browser_name == "chromium":
            if browser_channel:
                print(f"   Channel: {browser_channel}")
            browser = await p.chromium.launch(
                headless=check_headless_mode(),
                channel=browser_channel,
                slow_mo=50,
                ignore_default_args=["--disable-extensions"],
            )
        elif browser_name == "firefox":
            browser = await p.firefox.launch(
                headless=check_headless_mode(),
                slow_mo=50,
                ignore_default_args=["--disable-extensions"],
            )
        elif browser_name == "webkit":
            browser = await p.webkit.launch(
                headless=check_headless_mode(),
                slow_mo=50,
                ignore_default_args=["--disable-extensions"],
            )

        yield browser
        await browser.close()

@pytest.fixture
def browser_type_launch_args():
    print("🔧 Configuring browser launch arguments...")
    """Configure browser launch arguments - similar to 'projects' in playwright.config.ts"""
    return {
        "headless": check_headless_mode(),  # Set to True for headless, False for headed
        "slow_mo": 50,  # Slow down operations for debugging
        # Browser window - force maximized and visible
        "args": [
            "--start-maximized",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
            "--force-color-profile=srgb",
            "--new-window",
        ],
        # Downloads
        "downloads_path": "test-results/downloads/",
    }


def check_headless_mode():
    """
    Check if the browser is running in headless mode.
    This can be useful for debugging or conditional logic based on the mode.
    """
    headless = os.environ.get("HEADLESS", "true").lower() == "true"
    print(f"🔍 Running in headless mode: {headless}")
    return headless


def pytest_sessionfinish(session, exitstatus):
    """Clean up session files when pytest session finishes."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")


# JSON reporting hook - uncomment if pytest-json-report is properly installed
def pytest_json_runtest_metadata(item, call):
    """Add metadata to individual test runs for JSON reporting."""
    if call.when == "call":
        scenario_mark = item.get_closest_marker("scenario")
        if scenario_mark and scenario_mark.args:
            return {"scenario": scenario_mark.args[0]}
    return {}


def pytest_runtest_setup(item):
    """Print test description before each test runs"""
    for mark in item.iter_markers("scenario"):
        if mark.args:
            print(f"\n🧪 Test scenario: {mark.args[0]}")
            break


# ============================================================================
# PAGE OBJECT FIXTURES
# ============================================================================

@pytest.fixture
def all_pages():
    """
    Fixture to load all available page objects at once.

    Returns:
        Dictionary mapping page class names to their classes

    Usage in tests:
        def test_example(all_pages):
            # Access all pages with their class names
            dashboard = all_pages['ExamplePage'](page)
    """
    pages_dict = load_all_pages()
    print(f"✓ Loaded {len(pages_dict)} page object(s)")
    return pages_dict


@pytest.fixture
def pages_loader():
    """
    Fixture providing access to the PageLoader utility.
    
    Usage in tests:
        def test_example(page, pages_loader):
            DashboardPage = pages_loader.get_page('dashboard_page.DashboardPage')
            dashboard = DashboardPage(page)
    """
    return PageLoader


@pytest.fixture
def get_page_fixture():
    """
    Fixture providing convenient access to load page classes.
    
    Usage in tests:
        def test_example(get_page_fixture):
            DashboardPage = get_page_fixture('dashboard_page.DashboardPage')
    """
    return get_page


@pytest.fixture
def page_with_url(page: Page):
    """
    Fixture providing a page that has already navigated to BASE_URL.

    Returns:
        Playwright Page instance navigated to BASE_URL

    Usage in tests:
        def test_example(page_with_url, all_pages):
            dashboard = all_pages['ExamplePage'](page_with_url)
    """
    if BASE_URL:
        print(f"🌐 Navigating to: {BASE_URL}")
        page.goto(BASE_URL)
    return page


@pytest.fixture
def test_context(page: Page, all_pages, finnhub_request: APIRequestContext):
    """
    Unified fixture providing complete test context:
    - Browser page instance (already at BASE_URL)
    - All page objects loaded and ready to use
    - API request context for Finnhub

    Returns:
        Dictionary with keys: 'page', 'pages', 'api'

    Usage in tests:
        def test_example(test_context):
            page = test_context['page']
            page.goto(test_context['config']['base_url'])

            # Use page objects
            ExamplePage = test_context['pages']['ExamplePage']
            dashboard = ExamplePage(page)

            # Use API
            response = test_context['api'].get('/quote?symbol=AAPL')
    """
    if BASE_URL:
        print(f"🌐 Navigating to: {BASE_URL}")
        page.goto(BASE_URL)

    return {
        'page': page,
        'pages': all_pages,
        'api': finnhub_request,
        'config': {
            'base_url': BASE_URL,
            'finnhub_key': FINNHUB_KEY,
            'symbol': SYMBOL,
        }
    }



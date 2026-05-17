import pytest
import os
import sys
from pathlib import Path
from playwright.async_api import (
    async_playwright,
    Page as AsyncPage,
    APIRequestContext as AsyncAPIRequestContext,
)
from playwright.async_api import Playwright as AsyncPlaywright
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
    # only add --browser-channel if it doesn't exist
    try:
        parser.getgroup("playwright").addoption(
            "--browser-channel",
            action="store",
            default=None,
            help="Browser channel to use (e.g., msedge, chromium)",
        )
    except (ValueError, AttributeError):
        # Option might already exist or group doesn't exist, that's okay
        pass


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Start HTTP server for dashboard.html with proper lifecycle management"""
    project_root = Path(__file__).parent
    dashboard_dir = project_root / "dashboard"

    if not dashboard_dir.exists():
        dashboard_dir = project_root
        print(
            f"[INFO] Dashboard directory not found, using project root: {project_root}"
        )
    else:
        print(f"[INFO] Starting HTTP server in: {dashboard_dir}")

    proc = None
    try:
        proc = subprocess.Popen(
            ["python", "-m", "http.server", "8080"],
            cwd=str(dashboard_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        print(f"[OK] HTTP server started on port 8080")
        yield
    except Exception as e:
        print(f"[ERR] Failed to start HTTP server: {e}")
        yield
    finally:
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print(f"[OK] HTTP server terminated")
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"[OK] HTTP server killed (force)")
            except Exception as e:
                print(f"[WARN] Error terminating server: {e}")


@pytest.fixture(scope="session")
async def finnhub_request(playwright: AsyncPlaywright) -> AsyncAPIRequestContext:
    """
    Fixture providing API request context for Finnhub API (ASYNC).

    Creates a session-scoped API context that points to Finnhub API
    with the authentication token included in headers.

    Returns:
        Async APIRequestContext configured for Finnhub API
    """
    # Use Finnhub API base URL
    finnhub_api_url = "https://finnhub.io/api/v1"

    if not FINNHUB_KEY:
        print(
            "[WARN] FINNHUB_KEY not configured. API calls will fail without authentication."
        )

    print(f"[INFO] Creating Finnhub API context at: {finnhub_api_url}")

    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=finnhub_api_url,
            extra_http_headers={"X-Finnhub-Token": FINNHUB_KEY} if FINNHUB_KEY else {},
        )
        yield context
        await context.dispose()


@pytest.fixture(scope="session")
async def api_price(finnhub_request: AsyncAPIRequestContext) -> dict:
    """
    Fixture to fetch stock quote data from Finnhub API (ASYNC).

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
        print(f"[INFO] Fetching quote for symbol: {SYMBOL}")
        response = await finnhub_request.get(f"/quote?symbol={SYMBOL}")

        if not response.ok:
            print(f"[WARN] API Error: {response.status} - {response.text}")
            return {}

        data = await response.json()
        print(f"[OK] Quote fetched successfully for {SYMBOL}: ${data.get('c', 'N/A')}")
        return data
    except Exception as e:
        print(f"[ERR] Error fetching quote: {e}")
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


def check_headless_mode():
    """
    Check if the browser is running in headless mode.
    This can be useful for debugging or conditional logic based on the mode.
    """
    headless = EnvConfig.get("HEADLESS", "true").lower() == "true"
    print(f"[INFO] Running in headless mode: {headless}")
    return headless


# ===== ASYNC PLAYWRIGHT FIXTURES =====


@pytest.fixture
async def async_browser(browser_name, browser_channel):
    """Launch browser asynchronously with specified type and channel."""
    print(
        f"[INFO] Launching async browser: {browser_name} (headless={check_headless_mode()})"
    )

    async with async_playwright() as p:
        if browser_name == "chromium":
            if browser_channel:
                print(f"   Channel: {browser_channel}")
            browser = await p.chromium.launch(
                headless=check_headless_mode(),
                channel=browser_channel,
                slow_mo=50,
            )
        elif browser_name == "firefox":
            browser = await p.firefox.launch(
                headless=check_headless_mode(),
                slow_mo=50,
            )
        elif browser_name == "webkit":
            browser = await p.webkit.launch(
                headless=check_headless_mode(),
                slow_mo=50,
            )
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        yield browser
        await browser.close()


@pytest.fixture
async def async_context(async_browser):
    """Create async browser context."""
    context = await async_browser.new_context()
    yield context
    await context.close()


@pytest.fixture
async def async_page(async_context):
    """Create async page, navigate to BASE_URL, and inject DashboardPage."""
    page = await async_context.new_page()

    if BASE_URL:
        print(f"[INFO] Navigating to: {BASE_URL}")
        await page.goto(BASE_URL)

    yield page
    await page.close()


@pytest.fixture
async def async_api():
    """Create async API request context for Finnhub."""
    finnhub_api_url = "https://finnhub.io/api/v1"

    if not FINNHUB_KEY:
        print(
            "[WARN] FINNHUB_KEY not configured. API calls will fail without authentication."
        )

    print(f"[INFO] Creating async Finnhub API context at: {finnhub_api_url}")

    async with async_playwright() as p:
        context = await p.request.new_context(
            base_url=finnhub_api_url,
            extra_http_headers={"X-Finnhub-Token": FINNHUB_KEY} if FINNHUB_KEY else {},
        )
        yield context
        await context.dispose()


def pytest_sessionfinish(session, exitstatus):
    """Clean up session files when pytest session finishes."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "main")


# ===== PYTEST HOOKS =====


def pytest_runtest_setup(item):
    """Print test description before each test runs"""
    for mark in item.iter_markers("scenario"):
        if mark.args:
            print(f"\n[TEST] Scenario: {mark.args[0]}")
            break


# ===== PAGE FIXTURES (ASYNC) =====


@pytest.fixture
async def page_with_url(async_page: AsyncPage):
    """
    Fixture providing a page that has already navigated to BASE_URL (ASYNC).

    Returns:
        Async Playwright Page instance navigated to BASE_URL

    Usage in async tests:
        async def test_example(page_with_url):
            dashboard = DashboardPage(page_with_url)
    """
    if BASE_URL:
        print(f"[INFO] Navigating to: {BASE_URL}")
        await async_page.goto(BASE_URL)
    return async_page


@pytest.fixture
async def test_context(async_page: AsyncPage, async_api: AsyncAPIRequestContext):
    """
    Unified fixture providing complete test context (ASYNC):
    - Async browser page instance (already at BASE_URL)
    - All page objects loaded and ready to use
    - Async API request context for Finnhub

    Returns:
        Dictionary with keys: 'page', 'pages', 'api', 'config'

    Usage in async tests:
        async def test_example(test_context):
            page = test_context['page']
            api = test_context['api']

            from src.pages.dashboard_page import DashboardPage
            dashboard = DashboardPage(page)

            await dashboard.enter_api_key('your-key')
            response = await test_context['api'].get('/quote?symbol=AAPL')
    """
    if BASE_URL:
        print(f"[INFO] Navigating to: {BASE_URL}")
        await async_page.goto(BASE_URL)

    return {
        "page": async_page,
        "api": async_api,
        "config": {
            "base_url": BASE_URL,
            "finnhub_key": FINNHUB_KEY,
            "symbol": SYMBOL,
        },
    }

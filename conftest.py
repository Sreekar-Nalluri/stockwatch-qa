import pytest
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from api import FinnhubClient
from utils.env_config import EnvConfig
import subprocess
import socket
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

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
def start_server(tmp_path_factory, worker_id):
    def port_open():
        with socket.socket() as s:
            return s.connect_ex(("localhost", 8080)) == 0

    if port_open():
        yield
        return

    if worker_id != "gw0" and worker_id != "master":
        for _ in range(20):
            if port_open():
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("HTTP server never came up on port 8080")
        yield
        return

    project_root = Path(__file__).parent
    dashboard_dir = project_root / "dashboard"
    if not dashboard_dir.exists():
        dashboard_dir = project_root

    proc = subprocess.Popen(
        ["python", "-m", "http.server", "8080"],
        cwd=str(dashboard_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(20):
        if port_open():
            break
        time.sleep(0.5)
    else:
        proc.terminate()
        raise RuntimeError("HTTP server failed to start on port 8080")

    print("[OK] HTTP server started on port 8080")
    yield

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    print("[OK] HTTP server terminated")


@pytest.fixture(scope="session")
def finnhub_client():
    return FinnhubClient()


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


def pytest_runtest_setup(item):
    """Print test scenario before each test runs"""
    for mark in item.iter_markers("scenario"):
        if mark.args:
            print(f"\n[TEST] Scenario: {mark.args[0]}")
            break

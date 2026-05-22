import pytest
import sys
import socket
import time
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright
from api import FinnhubClient
from utils.env_config import EnvConfig

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Initialize environment variable loading
env_config = EnvConfig()

# Load configuration variables with fallback strategy
FINNHUB_KEY = EnvConfig.get("FINNHUB_KEY")
BASE_URL = EnvConfig.get("BASE_URL", "http://localhost:8080/dashboard.html")
SYMBOL = EnvConfig.get("SYMBOL", "AAPL")
BROWSER_TYPE = EnvConfig.get("BROWSER_TYPE", "chromium")


def pytest_addoption(parser):
    """Add command-line options for pytest."""
    try:
        parser.getgroup("playwright").addoption(
            "--browser-channel",
            action="store",
            default=None,
            help="Browser channel to use (e.g., msedge, chromium)",
        )
    except (ValueError, AttributeError):
        pass


# ------------------------------------------------------------------
# Server helpers
# ------------------------------------------------------------------

def _wait_for_port(host: str, port: int, timeout: int = 15):
    """
    Block until the port accepts TCP connections or timeout is reached.
    Replaces time.sleep(1) which is unreliable on cold CI runners.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return  # port is open and accepting connections
        except (ConnectionRefusedError, OSError):
            time.sleep(0.2)
    raise RuntimeError(
        f"HTTP server on {host}:{port} did not start within {timeout}s"
    )


def _is_xdist_worker(request) -> bool:
    """Return True when running inside a pytest-xdist worker process (gw0, gw1 …)."""
    return hasattr(request.config, "workerinput")


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def start_server(request):
    """
    Start HTTP server for dashboard.html with proper lifecycle management.
    """
    project_root = Path(__file__).parent
    dashboard_dir = project_root / "dashboard"

    if not dashboard_dir.exists():
        dashboard_dir = project_root
        print(f"[INFO] Dashboard directory not found, using project root: {project_root}")
    else:
        print(f"[INFO] Starting HTTP server in: {dashboard_dir}")

    if _is_xdist_worker(request):
        print("[INFO] xdist worker detected — waiting for server on port 8080 ...")
        _wait_for_port("localhost", 8080, timeout=15)
        print("[OK]   Server ready (worker)")
        yield
        return

    proc = None
    try:
        proc = subprocess.Popen(
            ["python", "-m", "http.server", "8080"],
            cwd=str(dashboard_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _wait_for_port("localhost", 8080, timeout=15)
        print("[OK]   HTTP server started on port 8080")
        yield
    except Exception as e:
        print(f"[ERR]  Failed to start HTTP server: {e}")
        yield
    finally:
        if proc:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print("[OK]   HTTP server terminated")
            except subprocess.TimeoutExpired:
                proc.kill()
                print("[OK]   HTTP server killed (force)")
            except Exception as ex:
                print(f"[WARN] Error terminating server: {ex}")


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


def check_headless_mode() -> bool:
    """Return True when HEADLESS env var is 'true' (default)."""
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
    """Print test scenario description before each test runs."""
    for mark in item.iter_markers("scenario"):
        if mark.args:
            print(f"\n[TEST] Scenario: {mark.args[0]}")
            break

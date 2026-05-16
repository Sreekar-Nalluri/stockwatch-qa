"""
SETUP AND USAGE GUIDE
=====================

This document explains how to use the new environment configuration system
and page object loader in this Playwright Finnhub automation framework.

## 1. ENVIRONMENT VARIABLE CONFIGURATION
====================================

The `EnvConfig` class automatically loads environment variables with this priority:

1. **Runtime Environment Variables** (highest priority)
   - Variables set directly in your OS environment or passed at runtime
   
2. **config/.env** (medium priority)
   - Default environment file for general configuration
   
3. **config/.env.local** (lowest priority)
   - Local override file (typically .gitignored for sensitive data)

### How to Use EnvConfig

#### Option A: Simple get() with default

```python
from src.utils.config import EnvConfig

# Returns value if found, otherwise returns default
base_url = EnvConfig.get("BASE_URL", "http://localhost:8080")
symbol = EnvConfig.get("SYMBOL", "AAPL")
```

#### Option B: get_required() - throws error if not found

```python
from src.utils.config import EnvConfig

# Raises ValueError if FINNHUB_KEY is not found anywhere
api_key = EnvConfig.get_required("FINNHUB_KEY")
```

#### Option C: Using in conftest.py (already set up)
```python
from config import EnvConfig

FINNHUB_KEY = EnvConfig.get("FINNHUB_KEY")
BASE_URL = EnvConfig.get("BASE_URL")
SYMBOL = EnvConfig.get("SYMBOL", "AAPL")
```

### Setting Environment Variables

#### Windows (PowerShell)
```powershell
# Runtime - for current session only
$env:FINNHUB_KEY = "your_key_here"
$env:BASE_URL = "http://localhost:8080"

# Permanent - add to config/.env or config/.env.local
# File: config/.env
FINNHUB_KEY=your_key_here
BASE_URL=http://localhost:8080
```

#### Linux/Mac (Bash)
```bash
# Runtime
export FINNHUB_KEY="your_key_here"
export BASE_URL="http://localhost:8080"

# Permanent - add to config/.env or config/.env.local
```


## 2. PAGE OBJECT LOADER
======================

The `PageLoader` dynamically loads page object classes from the `src/pages/` folder.
This allows you to organize your page objects and load them as needed.

### Creating a Page Object Class

Create a file in `src/pages/` with your page object class:

```python
# src/pages/dashboard_page.py
from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
    
    # Define locators
    @property
    def stock_ticker(self) -> str:
        return "input[data-testid='stock-ticker']"
    
    @property
    def search_button(self) -> str:
        return "button[data-testid='search-btn']"
    
    # Define action methods
    def search_stock(self, symbol: str) -> None:
        self.page.fill(self.stock_ticker, symbol)
        self.page.click(self.search_button)
    
    def get_current_price(self) -> str:
        return self.page.text_content("h2[data-testid='price']")
```

### Using Page Objects in Tests

#### Option A: Dynamic Loading with get_page_fixture
```python
# src/tests/test_dashboard.py
import pytest

@pytest.mark.scenario("Verify stock search")
def test_search_stock(page, get_page_fixture):
    # Dynamically load the page class
    DashboardPage = get_page_fixture('dashboard_page.DashboardPage')
    
    # Navigate and use
    page.goto("http://localhost:8080/dashboard.html")
    dashboard = DashboardPage(page)
    
    dashboard.search_stock("AAPL")
    price = dashboard.get_current_price()
    assert price is not None
```

#### Option B: Direct Import (static)
```python
# src/tests/test_dashboard.py
from src.pages.dashboard_page import DashboardPage

def test_search_stock(page):
    page.goto("http://localhost:8080/dashboard.html")
    dashboard = DashboardPage(page)
    
    dashboard.search_stock("AAPL")
    price = dashboard.get_current_price()
    assert price is not None
```

#### Option C: Load All Pages at Once
```python
def test_with_multiple_pages(pages_loader):
    # Discover all page objects
    all_pages = pages_loader.load_all_pages()
    
    # Use them as needed
    for page_name, page_class in all_pages.items():
        print(f"Found page: {page_name}")
```

### PageLoader Methods

#### get_page(page_path: str) -> Type

```python
from src.utils.pages_loader import get_page

# Load a specific page class
LoginPage = get_page('login_page.LoginPage')
DashboardPage = get_page('dashboard_page.DashboardPage')
```

#### load_all_pages() -> Dict[str, Type]

```python
from src.utils.pages_loader import load_all_pages

# Discover all page objects in src/pages/
pages = load_all_pages()
# Returns: {'LoginPage': <class>, 'DashboardPage': <class>, ...}
```

#### PageLoader.clear_cache()

```python
from src.utils.pages_loader import PageLoader

# Clear cached page classes (useful in fixtures for cleanup)
PageLoader.clear_cache()
```


## 3. FIXTURES AVAILABLE IN conftest.py
====================================

The following fixtures are automatically available in your tests:

### get_page_fixture
Provides convenient access to PageLoader.get_page()
```python
def test_example(get_page_fixture):
    DashboardPage = get_page_fixture('dashboard_page.DashboardPage')
```

### pages_loader
Provides access to the PageLoader class directly
```python
def test_example(pages_loader):
    all_pages = pages_loader.load_all_pages()
```

### Other Fixtures (from existing conftest.py)
- `browser`: Browser instance
- `finnhub_request`: API request context for Finnhub API
- `api_price`: Pre-fetched stock price data


## 4. PROJECT STRUCTURE
======================

```
playwright-finnhub/
├── config/
│   ├── .env              # Default environment variables
│   └── .env.local        # Local overrides (typically .gitignored)
├── src/
│   ├── config.py         # Environment configuration loader
│   ├── pages_loader.py   # Page object loader utility
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── example_page.py        # Example page object
│   │   ├── dashboard_page.py      # Your pages here
│   │   ├── login_page.py          # Add more as needed
│   │   └── ...
│   └── tests/
│       ├── __init__.py
│       ├── test_example.py        # Example tests
│       ├── test_dashboard.py      # Your tests here
│       └── ...
├── conftest.py           # Updated with new configuration
├── pyproject.toml
├── README.md
└── LICENSE
```


## 5. EXAMPLE WORKFLOW
====================

### Step 1: Create a Page Object
```python
# src/pages/login_page.py
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
    
    @property
    def username_field(self):
        return "input[name='username']"
    
    @property
    def password_field(self):
        return "input[name='password']"
    
    @property
    def login_button(self):
        return "button[type='submit']"
    
    def login(self, username: str, password: str):
        self.page.fill(self.username_field, username)
        self.page.fill(self.password_field, password)
        self.page.click(self.login_button)
```

### Step 2: Write a Test Using the Page Object

```python
# src/tests/test_login.py
import pytest
from src.utils.config import EnvConfig


@pytest.mark.scenario("User can login with valid credentials")
def test_valid_login(page, get_page_fixture):
   # Load the page object
   LoginPage = get_page_fixture('login_page.LoginPage')

   # Navigate to login page
   page.goto(EnvConfig.get("BASE_URL"))

   # Use the page object
   login_page = LoginPage(page)
   login_page.login("testuser", "password123")

   # Verify login was successful
   assert "dashboard" in page.url
```

### Step 3: Run the Test
```bash
# pytest will automatically discover and run your tests
pytest

# Run with specific browser
pytest --browser chromium

# Run in headed mode (see browser window)
# First set environment variable
$env:HEADLESS = "false"
pytest

# Or from config/.env
# HEADLESS=false
# SYMBOL=GOOGL
pytest
```


## 6. BEST PRACTICES
==================

1. **One page class per file**
   - File name: `dashboard_page.py`
   - Class name: `DashboardPage`

2. **Use properties for locators**
   ```python
   @property
   def search_input(self):
       return "input[data-testid='search']"
   ```

3. **Group related actions in methods**
   ```python
   def search_and_verify(self, query):
       self.fill_search(query)
       self.click_search()
       self.wait_for_results()
   ```

4. **Don't put assertions in page objects**
   - Page objects should navigate/interact
   - Tests should verify/assert

5. **Use meaningful method names**
   - Good: `click_submit_button()`, `get_user_name()`
   - Bad: `click()`, `text()`

6. **Document page object usage in docstrings**

7. **Keep tests focused on business logic**
   - Use page objects to abstract implementation details


## 7. TROUBLESHOOTING
===================

### "Cannot import page module"
- Check the module path is correct: `dashboard_page.DashboardPage`
- Verify the file exists: `src/pages/dashboard_page.py`
- Ensure the class is defined in that file

### "Required environment variable 'X' not found"
- Check if variable is set in runtime: `echo $env:FINNHUB_KEY` (Windows)
- Check in `config/.env`
- Check in `config/.env.local`
- Priority: runtime > config/.env > config/.env.local

### Page object methods not found
- Verify the class is instantiated: `page_obj = PageClass(page)`
- Don't call methods on the class itself

### Tests are slow to load page objects
- Page objects are cached, first load may be slower
- Subsequent loads are instantaneous
- Use `pytest -v` to see import times
"""


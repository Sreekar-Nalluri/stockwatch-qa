# stockwatch-qa

A **Python + Playwright** automation framework for validating real-time stock data in a custom-built UI dashboard. The dashboard fetches live prices via the **Finnhub API**, and this framework validates both the **UI layer** (via Playwright browser automation) and the **API layer** (via the official `finnhub` Python package) to ensure data accuracy and dashboard correctness.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher (3.13+ recommended)
- pip (Python package installer)
- Node.js (optional, for Playwright MCP)

---

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/Sreekar-Nalluri/playwright-finnhub.git
cd playwright-finnhub
```

#### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

#### 3. Install Python dependencies

```bash
pip install -e .
```

This installs all dependencies declared in `pyproject.toml`, including `playwright`, `finnhub-python`, `pytest`, and `python-dotenv`.

To install the `finnhub` package separately:

```bash
pip install finnhub-python
```

#### 4. Install Playwright browsers

```bash
playwright install
```

To install a specific browser only:

```bash
playwright install chromium     # or firefox / webkit
```

---

### 🔑 Configure your Finnhub API Key

The framework reads your Finnhub API key from a local environment file that is **never committed to source control**.

Create `config/.env.local` and add your key:

```bash
# config/.env.local
FINNHUB_KEY=your_actual_api_key_here
```

> **Get a free API key** at [https://finnhub.io](https://finnhub.io) → Sign up → Dashboard → API Key.

> `config/.env.local` is listed in `.gitignore` and will never be pushed to GitHub.

#### Available environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `FINNHUB_KEY` | ✅ Yes | — | Your Finnhub API key |
| `BASE_URL` | No | `http://localhost:8080/dashboard.html` | Dashboard URL under test |
| `SYMBOL` | No | `AAPL` | Default ticker symbol |
| `BROWSER_TYPE` | No | `chromium` | Browser: `chromium`, `firefox`, `webkit` |
| `HEADLESS` | No | `true` | Run browser headlessly (`true` / `false`) |
| `SERVER_PORT` | No | `8080` | Port for the local HTTP server |

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run with visible browser
HEADLESS=false pytest

# Run a specific test file
pytest tests/test_dashboard.py

# Run API-only tests (no browser)
pytest tests/api/

# Run with a different symbol
SYMBOL=TSLA pytest
```

---

## Playwright MCP — AI-Assisted UI Test Generation

[Playwright MCP](https://github.com/microsoft/playwright-mcp) lets AI assistants (Claude, Copilot, etc.) control a real browser and **generate Playwright tests** by observing the live dashboard UI.

### Install Playwright MCP

```bash
npm install -g @playwright/mcp
```

### `mcp.json` configuration

Create a `mcp.json` file in your project root (or in your AI editor's config directory):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser", "chromium",
        "--headless"
      ]
    }
  }
}
```

To run with a **visible browser** (useful when generating tests interactively):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser", "chromium"
      ]
    }
  }
}
```

### Integrate with Claude Desktop

1. Open **Claude Desktop** → Settings → Developer → Edit Config.
2. Add the `playwright` block from the `mcp.json` above into your `claude_desktop_config.json`.
3. Restart Claude Desktop.
4. Claude can now open the dashboard at `http://localhost:8080/dashboard.html`, inspect elements, and write Playwright tests based on what it sees.

### Integrate with VS Code (Copilot / Continue)

1. Install the **Continue** or **Copilot Chat** extension.
2. Add the `mcp.json` to your `.vscode/` folder or the extension's MCP config path.
3. The AI assistant will use the Playwright MCP server to browse and generate tests.

### Example: Generate a test with Claude

Start your local dashboard server first:

```bash
python -m http.server 8080 --directory dashboard/
```

Then ask Claude (with MCP connected):

> *"Go to http://localhost:8080/dashboard.html, find the stock price element for AAPL, and write a Playwright test that asserts the price is a positive number."*

Claude will navigate the real browser, inspect the DOM, and output a ready-to-use `pytest` test file.

---

## 🗂️ Project Structure

```
playwright-finnhub/
├── config/
│   ├── .env              # Shared non-secret defaults (committed)
│   └── .env.local        # Your secrets — NEVER committed
├── dashboard/
│   └── dashboard.html    # Custom stock dashboard UI
├── src/
│   ├── api/
│   │   └── finnhub_client.py   # finnhub Python package wrapper
│   └── utils/
│       ├── config.py           # EnvConfig — typed env var accessors
│       └── pages_loader.py     # Page Object loader
├── tests/
│   ├── api/              # Pure Python API validation tests
│   └── ui/               # Playwright browser tests
├── conftest.py           # Fixtures: server, browser, API client
├── mcp.json              # Playwright MCP configuration
└── pyproject.toml        # Dependencies and project metadata
```

---

## 🧪 How It Works

```
┌─────────────────────────────────────┐
│         pytest test session         │
│                                     │
│  conftest.py                        │
│  ├── start_server()  ──────────────►│  python -m http.server 8080
│  │                                  │  serves dashboard/dashboard.html
│  ├── finnhub_client fixture ───────►│  finnhub.Client(api_key=FINNHUB_KEY)
│  │                                  │
│  └── page fixture (Playwright) ────►│  browser → http://localhost:8080
│                                     │
│  tests/api/     → validate Finnhub API responses directly (no browser)
│  tests/ui/      → validate dashboard UI matches API data
└─────────────────────────────────────┘
```

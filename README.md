# stockwatch-qa

A **Python + Playwright** automation framework for validating real-time stock data in a custom-built UI dashboard. The dashboard fetches live prices via the **Finnhub API**, and this framework validates both the **UI layer** (via Playwright browser automation) and the **API layer** (via the official `finnhub` Python package) to ensure data accuracy and dashboard correctness.

---

## 🗂️ Project Structure

```
stockwatch-qa/
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

## Playwright MCP — AI-Assisted UI Test Generation

[Playwright MCP](https://github.com/microsoft/playwright-mcp) lets AI assistants control a real browser and **generate Playwright tests** by observing the live dashboard UI.

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

### Integrate with PyCharm / JetBrains IDEs

1. Open PyCharm → **Settings** → **Tools** → **GitHub Copilot** → **Model Context Protocol(MCP)** → click configure

2. Open PyCharm → **Settings** → **Plugins** →  **Marketplace** → Search for "GitHub Copilot" → Install and restart the IDE.

3. Add the MCP server config below in `.mcp.json`

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

4. Click GitHub Copilot chat icon on the right sidebar to open the chat window.

5. Select Agent and click configure tools icon, scroll down and check playwright to enable it.

6. Now give instructions to the Copilot agent in natural language, (type use playwright mcp in your prompt) and it will use the Playwright MCP server to interact with the dashboard UI and generate tests.

### Integrate with VS Code (Copilot / Continue)

1. Install the **Continue** or **Copilot Chat** extension.
2. Add the `mcp.json` to your `.vscode/` folder or the extension's MCP config path.
3. The AI assistant will use the Playwright MCP server to browse and generate tests.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher (3.12 recommended)
- pip (Python package installer)
- Node.js (optional, for Playwright MCP)

---

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/Sreekar-Nalluri/stockwatch-qa.git
cd stockwatch-qa
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
# config/.env.qa.local
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
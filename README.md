# pywright-finnhub
Playwright automation framework to validate real-time stock data using finnhub APIs

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher (3.13+ recommended)
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sreekar-Nalluri/playwright-finnhub.git
   cd playwright-finnhub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies from pyproject.toml**
   ```bash
   pip install -e .
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
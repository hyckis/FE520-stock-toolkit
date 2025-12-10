# FE520-stock-toolkit

# stocktoolkit

A simple Python package for downloading, analyzing, and visualizing stock price data.

The package is designed for beginners in Python and finance. It focuses on:

- Clean and readable code
- Basic time-series analysis of stock prices
- Robust input validation and error handling
- Clear plots for price and returns

No machine learning or web development is used, in line with the project requirements.

---

## 1. Installation

### 1.1. Requirements

- Python 3.10+ (or similar)
- Internet connection (for downloading data from Yahoo Finance)

Python packages used (all allowed by the assignment):

- `pandas`
- `numpy`
- `matplotlib`
- `yfinance`
- `datetime` (standard library)

### 1.2. Getting the code

If this project is hosted on GitHub, you can clone it:

```bash
git clone https://github.com/<your-username>/FE520-stock-toolkit.git
cd FE520-stock-toolkit

---

## 2. Project Structure
FE520-stock-toolkit/
│
├─ README.md                # Documentation (this file)
├─ demo.py                  # Example script demonstrating basic usage
├─ tests/                   # Unit tests for each module
│   ├─ test_validation.py
│   ├─ test_data.py
│   ├─ test_indicators.py
│   └─ test_plotting.py
│
└─ stocktoolkit/            # Python package
    ├─ __init__.py
    ├─ data.py              # Data download and preprocessing
    ├─ validation.py        # Centralized validation and error handling
    ├─ indicators.py        # Returns and technical indicators
    └─ plotting.py          # Visualization utilities

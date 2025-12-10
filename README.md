# FE520-stock-toolkit

A simple Python package for downloading, analyzing, and visualizing stock price data.

The package is designed for beginners in Python and finance. It focuses on:
- Clean and readable code
- Basic time-series analysis of stock prices
- Robust input validation and error handling
- Clear plots for price and returns


---

## 1. How to Use Our Package

### 1.1 Installation

#### Requirements

- Python 3.10+ (tested with Python 3.11.13)
- Internet connection (for downloading data from Yahoo Finance)

#### Install Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install yfinance pandas numpy matplotlib
```

#### Getting the Code

Clone or download this repository:

```bash
git clone https://github.com/<your-username>/FE520-stock-toolkit.git
cd FE520-stock-toolkit
```

### 1.2 Quick Start

Here's a simple example to get you started:

```python
from stocktoolkit import (
    download_price_data,
    get_close_price,
    compute_returns,
    plot_price,
    plot_returns,
)

# Download AAPL stock data
df = download_price_data("AAPL", "2024-01-01", "2024-06-30")

# Extract close price series
close = get_close_price(df)

# Compute simple returns
returns = compute_returns(close, method="simple")

# Plot price with moving averages
plot_price(close, ma_windows=[20, 60], title="AAPL Price with MAs")

# Plot returns
plot_returns(returns, title="AAPL Daily Returns")
```

### 1.3 Basic Usage Examples

#### Example 1: Download and Analyze Single Stock

```python
from stocktoolkit import download_price_data, get_close_price, compute_returns

# Download data
df = download_price_data("MSFT", "2024-01-01", "2024-12-31")

# Get close prices
close = get_close_price(df)

# Compute log returns
log_returns = compute_returns(close, method="log")
print(f"Average daily return: {log_returns.mean():.4f}")
```

#### Example 2: Multiple Stocks Analysis

```python
from stocktoolkit import download_multiple_price_data, get_close_price

# Download multiple stocks
symbols = ["AAPL", "MSFT", "GOOGL"]
data_dict = download_multiple_price_data(symbols, "2024-01-01", "2024-06-30")

# Extract close prices for each stock
for symbol, df in data_dict.items():
    close = get_close_price(df)
    print(f"{symbol} - Latest price: ${close.iloc[-1]:.2f}")
```



## 2. Introduction of Modules

The package consists of four main modules:

### 2.1 `data` Module

**Purpose**: Download stock price data and perform basic preprocessing.

**Key Functions**:

- **`download_price_data(symbol, start_date, end_date, interval="1d")`**
  - Downloads OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance
  - Parameters:
    - `symbol`: Stock ticker symbol (e.g., "AAPL")
    - `start_date`: Start date in "YYYY-MM-DD" format
    - `end_date`: End date in "YYYY-MM-DD" format
    - `interval`: Data frequency ("1d", "1wk", "1mo")
  - Returns: `pd.DataFrame` with DateTimeIndex
  - Raises: `ValueError` if dates are invalid or no data is returned

- **`download_multiple_price_data(symbols, start_date, end_date, interval="1d")`**
  - Downloads data for multiple stocks simultaneously
  - Parameters:
    - `symbols`: List or tuple of ticker symbols
    - Other parameters same as above
  - Returns: Dictionary mapping symbol → DataFrame

- **`get_close_price(df, use_adjusted=True)`**
  - Extracts close price series from a price DataFrame
  - Prefers "Adj Close" if available (default), otherwise uses "Close"
  - Returns: `pd.Series` with DateTimeIndex
  - Raises: `ValueError` if neither column exists

- **`resample_price(df, freq="W", how="last")`**
  - Resamples price data to different frequencies (weekly, monthly, etc.)
  - Parameters:
    - `freq`: Resample frequency ("W" for weekly, "M" for monthly)
    - `how`: Aggregation method ("last", "first", or "mean")
  - Returns: Resampled `pd.DataFrame`

**Dependencies**: `yfinance`, `pandas`, `datetime`

---

### 2.2 `indicators` Module

**Purpose**: Calculate technical indicators and returns for stock price analysis.

**Key Functions**:

- **`compute_returns(price_series, method="simple")`**
  - Calculates returns from a price series
  - Parameters:
    - `price_series`: `pd.Series` with DateTimeIndex
    - `method`: "simple" for percentage returns or "log" for logarithmic returns
  - Returns: `pd.Series` of returns (first value is NaN)
  - Formula:
    - Simple: `r_t = (P_t - P_{t-1}) / P_{t-1}`
    - Log: `r_t = ln(P_t / P_{t-1})`
  - Raises: `ValueError` for unsupported methods, `TypeError` for invalid input types

- **`moving_average(price_series, window)`**
  - Calculates simple moving average (SMA)
  - Parameters:
    - `price_series`: `pd.Series` with DateTimeIndex
    - `window`: Integer window size (e.g., 20 for 20-day MA)
  - Returns: `pd.Series` with moving average values
  - Raises: `TypeError` if window is not an integer, `ValueError` if window ≤ 0

- **`rolling_volatility(return_series, window)`**
  - Calculates rolling standard deviation (volatility proxy)
  - Parameters:
    - `return_series`: `pd.Series` of returns
    - `window`: Integer window size
  - Returns: `pd.Series` of rolling volatility
  - Raises: Same validation errors as `moving_average`

**Dependencies**: `pandas`, `numpy`

---

### 2.3 `plotting` Module

**Purpose**: Create visualizations for stock prices and returns.

**Key Functions**:

- **`plot_price(price_series, ma_windows=None, title=None)`**
  - Plots a price series with optional moving average overlays
  - Parameters:
    - `price_series`: `pd.Series` with DateTimeIndex
    - `ma_windows`: Optional list of integers (e.g., [20, 60] for 20-day and 60-day MAs)
    - `title`: Optional plot title
  - Features:
    - Price line in blue
    - Moving averages in different colors with labels
    - Grid, legend, and formatted axes
  - Raises: `TypeError` if input is not a Series

- **`plot_returns(return_series, title=None)`**
  - Plots a return series as a time series
  - Parameters:
    - `return_series`: `pd.Series` of returns
    - `title`: Optional plot title
  - Features:
    - Returns line in blue
    - Red dashed zero reference line
    - Grid and formatted axes
  - Raises: `TypeError` if input is not a Series

**Dependencies**: `matplotlib`, `pandas`

---

### 2.4 `validation` Module

**Purpose**: Centralized input validation and error handling.

**Key Functions**:

- **`validate_date_string(date_str)`**
  - Validates date string format ("YYYY-MM-DD")
  - Raises: `ValueError` if format is invalid

- **`validate_price_dataframe(df, symbol=None)`**
  - Checks if DataFrame is non-empty and has DateTimeIndex
  - Raises: `ValueError` if empty or invalid index

- **`validate_price_series(price_series)`**
  - Validates that input is a non-empty pandas Series with DateTimeIndex
  - Raises: `TypeError` or `ValueError` for invalid inputs

- **`validate_ma_window(window)`**
  - Validates moving average window is a positive integer
  - Raises: `TypeError` or `ValueError` for invalid inputs

- **`validate_symbols(symbols)`**
  - Normalizes and validates stock symbols
  - Returns: List of valid symbol strings
  - Raises: `ValueError` if no valid symbols provided

**Dependencies**: `pandas`, `datetime`

---

## 3. Test Cases

### 3.1 Running Tests

All tests are located in the `tests/` directory. To run all tests:

```bash
python -m unittest discover tests
```

To run a specific test file:

```bash
python -m unittest tests.test_data
python -m unittest tests.test_indicators
python -m unittest tests.test_plotting
python -m unittest tests.test_validation
```

To run with verbose output:

```bash
python -m unittest discover tests -v
```

### 3.2 Test Coverage

#### `test_data.py` - Data Module Tests

Tests cover:

- **`download_price_data`**:
  - ✅ Valid data download (returns DataFrame with DateTimeIndex)
  - ✅ Invalid date format (raises ValueError)
  - ✅ Invalid date range (end before start, raises ValueError)

- **`download_multiple_price_data`**:
  - ✅ Valid multiple downloads (returns dictionary with normalized symbols)
  - ✅ Invalid dates (raises ValueError)

- **`get_close_price`**:
  - ✅ Prefers "Adj Close" when available
  - ✅ Falls back to "Close" if no "Adj Close"
  - ✅ Raises ValueError if neither column exists

- **`resample_price`**:
  - ✅ Resampling with "last" method
  - ✅ Resampling with "first" method (case-insensitive)
  - ✅ Resampling with "mean" method
  - ✅ Invalid "how" parameter (raises ValueError)

#### `test_indicators.py` - Indicators Module Tests

Tests cover:

- **`compute_returns`**:
  - ✅ Simple returns calculation (correct values)
  - ✅ Log returns calculation (correct values)
  - ✅ Invalid method (raises ValueError)
  - ✅ Invalid input type (raises TypeError)

- **`moving_average`**:
  - ✅ Valid MA calculation (correct values, NaN handling)
  - ✅ Invalid window type (raises TypeError)
  - ✅ Invalid window value (raises ValueError for window ≤ 0)
  - ✅ Invalid input type (raises TypeError)

- **`rolling_volatility`**:
  - ✅ Valid volatility calculation
  - ✅ Invalid window type (raises TypeError)
  - ✅ Invalid window value (raises ValueError)
  - ✅ Invalid input type (raises TypeError)

#### `test_plotting.py` - Plotting Module Tests

Tests cover:

- **`plot_price`**:
  - ✅ Valid price series plotting
  - ✅ Plotting with moving averages
  - ✅ Invalid input type (raises TypeError)

- **`plot_returns`**:
  - ✅ Valid returns series plotting
  - ✅ Invalid input type (raises TypeError)

#### `test_validation.py` - Validation Module Tests

Tests cover:

- **`validate_date_string`**:
  - ✅ Valid date formats
  - ✅ Invalid date formats (raises ValueError)

- **`validate_price_dataframe`**:
  - ✅ Valid DataFrame
  - ✅ Empty DataFrame (raises ValueError)
  - ✅ Invalid index type (raises ValueError)

- **`validate_price_series`**:
  - ✅ Valid Series
  - ✅ Invalid type (raises TypeError)
  - ✅ Empty Series (raises ValueError)
  - ✅ Series with only NaN (raises ValueError)

- **`validate_ma_window`**:
  - ✅ Valid window values
  - ✅ Invalid type (raises TypeError)
  - ✅ Invalid value (raises ValueError)

- **`validate_symbols`**:
  - ✅ Single symbol string
  - ✅ List of symbols
  - ✅ Empty input (raises ValueError)

### 3.3 Test Structure

All tests use Python's `unittest` framework. Each test file contains:

- A test class inheriting from `unittest.TestCase`
- `setUp()` method for common test data (where applicable)
- Individual test methods prefixed with `test_`
- Assertions to verify expected behavior
- Tests for both valid inputs and error cases

### 3.4 Example Test Output

When running tests successfully, you should see:

```
.....
----------------------------------------------------------------------
Ran 5 tests in 2.345s

OK
```

If tests fail, the output will show which test failed and why, helping with debugging.

---

## Project Structure

```
FE520-stock-toolkit/
│
├── README.md                # This file
├── requirements.txt         # Package dependencies
├── demo.py                  # Example script demonstrating basic usage
│
├── stocktoolkit/            # Python package
│   ├── __init__.py          # Package initialization and exports
│   ├── data.py              # Data download and preprocessing
│   ├── validation.py        # Centralized validation and error handling
│   ├── indicators.py        # Returns and technical indicators
│   └── plotting.py          # Visualization utilities
│
└── tests/                   # Unit tests
    ├── test_data.py
    ├── test_indicators.py
    ├── test_plotting.py
    └── test_validation.py
```

---

## Error Handling

The package includes comprehensive error handling:

- **Invalid dates**: Raises `ValueError` with clear message about expected format
- **Invalid ticker symbols**: Raises `ValueError` when no data is returned
- **Type errors**: Raises `TypeError` when wrong data types are provided
- **Empty data**: Raises `ValueError` when DataFrames or Series are empty
- **Invalid parameters**: Raises `ValueError` for unsupported parameter values

All error messages are designed to be helpful for debugging and learning.

---



## Contributors

- Bin Xiao
- YiChin Ho

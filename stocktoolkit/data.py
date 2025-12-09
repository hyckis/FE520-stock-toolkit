"""
data.py
Data downloading and basic preprocessing utilities for stocktoolkit package
"""
from datetime import datetime

import pandas as pd
import yfinance as yf

from .validation import(
    validate_date_string,
    validate_price_dataframe,
    validate_symbols,
)

"""
Download price data for a single symbol from yfinance
-Parameters
--symbol: str
  Ticker symbol, e.g. "AAPL".
--start_date: str
  Start date in YYYY-MM-DD format.
--end_date: str
  End date in YYYY-MM-DD format.
--interval: str = "id"
  Data interval, e.g. "1d", "1wk", "1mo".
-Return pd.DataFrame: OHLCV data with a DateTimeIndex.
-Raise ValueError if the date format is invalid or no data is returned.
"""
def download_price_data(
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "id",
) -> pd.DataFrame:
    
    # Deal with uppercase/lowercase
    symbol = symbol.strip().upper()
    interval.strip().lower()
    
    # Validate input dates
    validate_date_string(start_date)
    validate_date_string(end_date)

    # Download data with yfinance
    df = yf.download(symbol, start=start_date, end=end_date, interval=interval)

    # Validate data is not empty and index is date-like
    validate_price_dataframe(df, symbol)

    # Ensure index is a DateTimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    return df

"""
Download price data for multiple symbols from yfinance
-Parameters
--symbol: str
  Ticker symbol, e.g. "AAPL".
--start_date: str
  Start date in YYYY-MM-DD format.
--end_date: str
  End date in YYYY-MM-DD format.
--interval: str = "id"
  Data interval, e.g. "1d", "1wk", "1mo".
-Returns dict[str, pd.DataFrame]: Mapping from symbol -> price DataFrame.
"""
def download_multiple_price_data(
    symbols: list[str] | tuple[str, ...],
    start_date: str,
    end_date: str,
    interval: str = "id",
) -> dict[str, pd.DataFrame]:
    
    # Deal with uppercase/lowercase
    interval.strip().lower()
    # Validate data is not empty and index is date-like
    valid_symbols = validate_symbols(symbols)
    
    # Validate input dates
    validate_date_string(start_date)
    validate_date_string(end_date)

    # Prepare results for return
    result: dict[str, pd.DataFrame] = {}
    for sym in valid_symbols:
        df = yf.download(sym, start=start_date, end=end_date, interval=interval)
        validate_price_dataframe(df, sym)
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        result[sym] = df

    return result

"""
Extract a clean close-price series from a price dataframe.
-Parameters
--df: pd.DataFrame
  OHLCV data.
--use_adjusted: bool, default=True
  if True, prefer 'Adj Close' when available.
-Returns
--pd.Series: close price series with DateTimeIndex.
-Raises ValueError if neither 'Adj Close' nor 'Close' is available.
"""
def get_close_price(df: pd.DataFrame, use_adjusted: bool = True) -> pd.Series:
    
    validate_price_dataframe(df)

    if use_adjusted and "Adj Close" in df.columns:
        series = df["Adj Close"]
    elif "Close" in df.columns:
        series = df["Close"]
    else:
        raise ValueError(
            "DataFrame must contain either 'Adj Close' or 'Close' column."
        )
    
    # Ensure it's a proper series with DateTimeIndex
    if not isinstance(series.index, pd.DatetimeIndex):
        series.index = pd.to_datetime(series.index)

    # Rename the series for nicer plotting / debugging
    series.name = "Close"

    return series

"""
Resample
-Parameters
--df: pd.DataFrame
--freq: str
  Default value: "W"
  Resample frequency, e.g. "W" (weekly), "M" (month-end).
--how: str
  Default value: "last"
  Options: "last", "first", "mean"
-Returns resampled
"""
def resample_price(
    df: pd.DataFrame,
    freq: str = "W",
    how: str = "last",
) -> pd.DataFrame:
    
    validate_price_dataframe(df)

    # Deal with uppercase/lowercase
    freq.strip().upper()
    how.strip().lower()

    if how == "last":
        resampled = df.resample(freq).last()
    elif how =="first":
        resampled = df.resample(freq).first()
    elif how == "mean":
        resampled = df.resample(freq).mean()
    else:
        raise ValueError(
            f"Unsupported 'how' value: {how!r}. Use 'last', 'first', or 'mean'."
        )

    return resampled
    
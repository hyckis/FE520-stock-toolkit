"""
validation.py
Input validation & Error handling for stocktoolkit package
"""

from datetime import datetime
from typing import Iterable

import pandas as pd

"""
Validate date string is in 'YYYY-MM-DD' format.
-Raises ValueError if the string is not in the correct format.
"""
def validate_date_string(date_str: str) -> None:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            f"Invalid date string: {date_str!r}. Expected format 'YYYY-MM-DD'."
        ) from exc

"""
Validate that the downloaded price dataframe is not empty and has a DateTimeIndex.
-Parameters:
--df : pd.DataFrame -> DataFrame returned from data download.
--symbol : str, optional -> Symbol used to download the data.
-Raises ValueError if the DataFrame is empty or index is not a DateTimeIndex.
"""
def validate_price_dataframe(df: pd.DataFrame, symbol: str | None = None) -> None:
    if df is None or df.empty:
        if symbol:
            raise ValueError(
                f"No data returned for symbol: {symbol!r}."
            )
        raise ValueError("No data returned.")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(
            "Price DataFrame must have a DateTimeIndex. "
            "Make sure you are using the date column as index."
        )  
    
"""
Validate that the input is a non-empty price series with a DateTimeIndex.
-Raises TypeError if the input is not a pandas Series
-Raises ValueError if the series is empty or contains only NaN values.
"""
def validate_price_series(price_series: pd.Series) -> None:
    if not isinstance(price_series, pd.Series):
        raise TypeError(
            f"price_series must be a pandas Series, got {type(price_series)} instead."
        )
    if price_series.empty:
        raise ValueError("price_series is empty.")
    if not isinstance(price_series.index, pd.DatetimeIndex):
        raise ValueError("price_series must have a DateTimeIndex.")
    if price_series.dropna().empty:
        raise ValueError("price_series contains only NaN values.")
    
"""
Validate that window is an positive integer
-Raise TypeError if window is not an integer
-Raise ValueError if window is not positive
"""
def validate_ma_window(window: int) -> None:
    if not isinstance(window, int):
        raise TypeError(f"window must be an int, got {type(window)} instead.")
    if window <= 0:
        raise ValueError("window must be a positive integer.")

"""
Normalize and validate symbol(s).
-Parameters
--symbols: str or iterable of str
-Returns list[str]
-Raise ValueError if no valid symbols are provided.
"""
def validate_symbols(symbols: str | Iterable[str]) -> list[str]:
    if isinstance(symbols, str):
        result = [symbols]
    else:
        result = [s for s in symbols if isinstance(s, str)]
    if not result:
        raise ValueError("At least one valid symbol (string) must be provided.")
    return result



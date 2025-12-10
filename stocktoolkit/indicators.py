"""
indicators.py
Return and technical indicator calculations for stocktoolkit.
"""

import numpy as np
import pandas as pd

from .validation import validate_price_series, validate_ma_window

"""
Compute simple or log returns from a price series.
-Parameters
--price_series : pd.Series
  Price series with DateTimeIndex.
--method : {"simple", "log"}, default "simple"
-Returns pd.Series
 Return series aligned with the original index.
"""
def compute_returns(price_series: pd.Series, method: str = "simple") -> pd.Series:
    validate_price_series(price_series)
    
    if method == "simple":
        returns = price_series.pct_change().dropna()
    elif method == "log":
        returns = np.log(price_series / price_series.shift(1)).dropna()
    else:
        raise ValueError(f"Unsupported method: {method!r}. Use 'simple' or 'log'.")
    
    return returns

"""
Compute a simple moving average over a given window.
-Parameters
--price_series : pd.Series
--window : int
-Returns pd.Series
"""
def moving_average(price_series: pd.Series, window: int) -> pd.Series:
    validate_price_series(price_series)
    validate_ma_window(window)
    
    return price_series.rolling(window=window).mean()

"""
Compute rolling volatility (standard deviation) of returns.
-Parameters
--return_series : pd.Series
  Return series.
--window : int
  Rolling window size.
-Returns
--pd.Series
"""
def rolling_volatility(return_series: pd.Series, window: int) -> pd.Series:
    validate_price_series(return_series)
    validate_ma_window(window)
    
    return return_series.rolling(window=window).std()




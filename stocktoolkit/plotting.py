"""
plotting.py
Visualization utilities for stocktoolkit.
"""

from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from .validation import validate_price_series
from .indicators import moving_average

"""
Plot a price series with optional moving-average overlays.
-Parameters
--price_series: pd.Series
--ma_windows: iterable of int, optional
  Window sizes for moving averages.
--title : str, optional
"""
def plot_price(
    price_series: pd.Series,
    ma_windows: Iterable[int] | None = None,
    title: str | None = None,
) -> None:
    validate_price_series(price_series)
    
    plt.figure(figsize=(12, 6))
    plt.plot(price_series.index, price_series.values, label="Price", linewidth=2)
    
    if ma_windows:
        for window in ma_windows:
            ma = moving_average(price_series, window)
            plt.plot(ma.index, ma.values, label=f"MA({window})", alpha=0.7)
    
    plt.xlabel("Date")
    plt.ylabel("Price")
    if title:
        plt.title(title)
    else:
        plt.title(f"{price_series.name} Price Chart")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

"""
-Parameters
--return_series : pd.Series
--title : str, optional
"""
def plot_returns(return_series: pd.Series, title: str | None = None) -> None:
    validate_price_series(return_series)
    
    plt.figure(figsize=(12, 6))
    plt.plot(return_series.index, return_series.values, linewidth=1, alpha=0.7)
    plt.axhline(y=0, color='r', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.xlabel("Date")
    plt.ylabel("Returns")
    if title:
        plt.title(title)
    else:
        plt.title(f"{return_series.name if return_series.name else 'Returns'} Chart")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()



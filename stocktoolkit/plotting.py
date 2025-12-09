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
    
"""
-Parameters
--return_series : pd.Series
--title : str, optional
"""
def plot_returns(return_series: pd.Series, title: str | None = None) -> None:



"""
stocktoolkit
A simple Python package for stock data analysis.
"""

from .data import (
    download_price_data,
    download_multiple_price_data,
    get_close_price,
    resample_price,
)

from .indicators import (
    compute_returns,
    moving_average,
    rolling_volatility,
)

from .plotting import (
    plot_price,
    plot_returns,
)

__all__ = [
    # data
    "download_price_data",
    "download_multiple_price_data",
    "get_close_price",
    "resample_price",
    # indicators
    "compute_returns",
    "moving_average",
    "rolling_volatility",
    # plotting
    "plot_price",
    "plot_returns",
]
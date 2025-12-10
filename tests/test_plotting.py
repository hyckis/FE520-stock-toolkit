import unittest

import matplotlib
matplotlib.use("Agg")  # use non-GUI backend for testing

import matplotlib.pyplot as plt
import pandas as pd

from stocktoolkit.plotting import (
    plot_price,
    plot_returns,
)


class TestPlottingModule(unittest.TestCase):
    def setUp(self):
        self.idx = pd.date_range("2024-01-01", periods=5, freq="D")
        self.prices = pd.Series([10.0, 10.5, 11.0, 10.0, 9.5], index=self.idx, name="TEST")
        self.returns = self.prices.pct_change().dropna()
        self.returns.name = "TEST_RETURNS"

    # ---------- plot_price ----------

    def test_plot_price_basic(self):
        # Should not raise any errors
        plot_price(self.prices, ma_windows=None, title="Basic Price Plot")

    def test_plot_price_with_ma(self):
        # Should handle moving-average overlays without error
        plot_price(self.prices, ma_windows=[2, 3], title="Price with MAs")

    def test_plot_price_invalid_input_type(self):
        with self.assertRaises(TypeError):
            plot_price([10.0, 10.5, 11.0])  # not a Series

    # ---------- plot_returns ----------

    def test_plot_returns_basic(self):
        plot_returns(self.returns, title="Returns Plot")

    def test_plot_returns_invalid_input_type(self):
        with self.assertRaises(TypeError):
            plot_returns([0.1, 0.2, -0.1])


if __name__ == "__main__":
    unittest.main()

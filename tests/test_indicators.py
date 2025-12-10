import unittest
import numpy as np
import pandas as pd

from stocktoolkit.indicators import (
    compute_returns,
    moving_average,
    rolling_volatility,
)


class TestIndicatorsModule(unittest.TestCase):
    def setUp(self):
        # Common price series for tests
        self.idx = pd.date_range("2024-01-01", periods=5, freq="D")
        self.prices = pd.Series([10.0, 10.5, 11.0, 10.0, 9.5], index=self.idx)

    # ---------- compute_returns ----------

    def test_compute_returns_simple(self):
        returns = compute_returns(self.prices, method="simple")
        self.assertIsInstance(returns, pd.Series)
        # After pct_change + dropna, length should be len(prices) - 1
        self.assertEqual(len(returns), len(self.prices) - 1)
        # Check first value manually
        expected_first = (10.5 - 10.0) / 10.0
        self.assertAlmostEqual(returns.iloc[0], expected_first, places=8)

    def test_compute_returns_log(self):
        returns = compute_returns(self.prices, method="log")
        self.assertIsInstance(returns, pd.Series)
        self.assertEqual(len(returns), len(self.prices) - 1)
        expected_first = np.log(10.5 / 10.0)
        self.assertAlmostEqual(returns.iloc[0], expected_first, places=8)

    def test_compute_returns_invalid_method(self):
        with self.assertRaises(ValueError):
            compute_returns(self.prices, method="SIMPLE")  # unsupported (case-sensitive)

    def test_compute_returns_invalid_input_type(self):
        with self.assertRaises(TypeError):
            compute_returns([10.0, 10.5, 11.0])  # not a Series

    # ---------- moving_average ----------

    def test_moving_average_valid(self):
        ma = moving_average(self.prices, window=2)
        self.assertIsInstance(ma, pd.Series)
        self.assertEqual(len(ma), len(self.prices))
        # First value should be NaN for window=2
        self.assertTrue(np.isnan(ma.iloc[0]))
        # Second value = (10 + 10.5) / 2 = 10.25
        self.assertAlmostEqual(ma.iloc[1], (10.0 + 10.5) / 2.0, places=8)

    def test_moving_average_invalid_window_type(self):
        with self.assertRaises(TypeError):
            moving_average(self.prices, window=2.5)

    def test_moving_average_invalid_window_value(self):
        with self.assertRaises(ValueError):
            moving_average(self.prices, window=0)

    def test_moving_average_invalid_series_type(self):
        with self.assertRaises(TypeError):
            moving_average([10.0, 10.5], window=2)

    # ---------- rolling_volatility ----------

    def test_rolling_volatility_valid(self):
        # Use simple returns as input
        returns = compute_returns(self.prices, method="simple")
        vol = rolling_volatility(returns, window=2)
        self.assertIsInstance(vol, pd.Series)
        self.assertEqual(len(vol), len(returns))

    def test_rolling_volatility_invalid_window_type(self):
        returns = compute_returns(self.prices, method="simple")
        with self.assertRaises(TypeError):
            rolling_volatility(returns, window="3")

    def test_rolling_volatility_invalid_window_value(self):
        returns = compute_returns(self.prices, method="simple")
        with self.assertRaises(ValueError):
            rolling_volatility(returns, window=0)

    def test_rolling_volatility_invalid_series_type(self):
        with self.assertRaises(TypeError):
            rolling_volatility([0.1, 0.2, -0.1], window=2)


if __name__ == "__main__":
    unittest.main()

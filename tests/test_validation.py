import unittest
from datetime import datetime

import pandas as pd

from stocktoolkit.validation import (
    validate_date_string,
    validate_price_dataframe,
    validate_price_series,
    validate_ma_window,
    validate_symbols,
)


class TestValidationModule(unittest.TestCase):
    # ---------- validate_date_string ----------

    def test_validate_date_string_valid(self):
        # Should not raise for valid format
        validate_date_string("2024-01-01")
        validate_date_string("1999-12-31")

    def test_validate_date_string_invalid(self):
        # Invalid month / day / format should raise ValueError
        with self.assertRaises(ValueError):
            validate_date_string("2024-13-01")
        with self.assertRaises(ValueError):
            validate_date_string("2024-00-10")
        with self.assertRaises(ValueError):
            validate_date_string("01-01-2024")
        with self.assertRaises(ValueError):
            validate_date_string("2024/01/01")

    # ---------- validate_price_dataframe ----------

    def test_validate_price_dataframe_valid(self):
        idx = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, index=idx)
        # Should not raise
        validate_price_dataframe(df, symbol="AAPL")

    def test_validate_price_dataframe_empty(self):
        df = pd.DataFrame()
        with self.assertRaises(ValueError):
            validate_price_dataframe(df, symbol="AAPL")

    def test_validate_price_dataframe_non_datetime_index(self):
        df = pd.DataFrame({"Close": [1, 2, 3]}, index=[1, 2, 3])
        with self.assertRaises(ValueError):
            validate_price_dataframe(df, symbol="AAPL")

    # ---------- validate_price_series ----------

    def test_validate_price_series_valid(self):
        idx = pd.date_range("2024-01-01", periods=3, freq="D")
        s = pd.Series([10.0, 11.0, 12.0], index=idx)
        validate_price_series(s)  # should not raise

    def test_validate_price_series_not_series(self):
        data = [1, 2, 3]
        with self.assertRaises(TypeError):
            validate_price_series(data)

    def test_validate_price_series_empty(self):
        s = pd.Series(dtype=float)
        with self.assertRaises(ValueError):
            validate_price_series(s)

    def test_validate_price_series_non_datetime_index(self):
        s = pd.Series([1, 2, 3], index=[1, 2, 3])
        with self.assertRaises(ValueError):
            validate_price_series(s)

    def test_validate_price_series_all_nan(self):
        idx = pd.date_range("2024-01-01", periods=3, freq="D")
        s = pd.Series([float("nan")] * 3, index=idx)
        with self.assertRaises(ValueError):
            validate_price_series(s)

    # ---------- validate_ma_window ----------

    def test_validate_ma_window_valid(self):
        validate_ma_window(1)
        validate_ma_window(20)

    def test_validate_ma_window_non_int(self):
        with self.assertRaises(TypeError):
            validate_ma_window(2.5)
        with self.assertRaises(TypeError):
            validate_ma_window("10")

    def test_validate_ma_window_non_positive(self):
        with self.assertRaises(ValueError):
            validate_ma_window(0)
        with self.assertRaises(ValueError):
            validate_ma_window(-5)

    # ---------- validate_symbols ----------

    def test_validate_symbols_single_string(self):
        symbols = validate_symbols(" aapl ")
        self.assertEqual(symbols, ["AAPL"])

    def test_validate_symbols_list_mixed_case_and_spaces(self):
        symbols = validate_symbols([" aapl ", "MsFt", " nvda  "])
        self.assertEqual(symbols, ["AAPL", "MSFT", "NVDA"])

    def test_validate_symbols_invalid_or_empty(self):
        with self.assertRaises(ValueError):
            validate_symbols([])

        with self.assertRaises(ValueError):
            validate_symbols(["   ", ""])


if __name__ == "__main__":
    unittest.main()
